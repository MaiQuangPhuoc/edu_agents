"""PDF is stored for viewing; prepared Markdown is the only indexing source."""
import hashlib
import json
import logging
import uuid
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

from .sources import DEFAULT_OUTPUT_ROOT, DEFAULT_SOURCE_ROOT, select_sources
from .collections import DEFAULT_COLLECTION_NAME

logger = logging.getLogger(__name__)


def validate_lesson_plan_name(name):
    name = unicodedata.normalize('NFC', str(name)).strip()
    if not name or len(name) > 200 or any(ord(char) < 32 for char in name):
        raise ValueError('Tên giáo án phải có 1–200 ký tự, không chứa ký tự điều khiển.')
    return name


class AutoIndexingError(RuntimeError):
    def __init__(self, message, report_path, status_code=422):
        super().__init__(message)
        self.report_path = report_path
        self.status_code = status_code


def run_auto_indexing(pdf_path, *, book_name, original_filename=None, source_root=None,
                      output_root=None, upload=True, batch_size=16,
                      source_subject=None, source_series=None, on_progress=None):
    name = validate_lesson_plan_name(book_name)
    lesson_plan_id = str(uuid.uuid5(uuid.NAMESPACE_URL, 'eduagent:lesson-plan:' + name.casefold()))
    pdf_path = Path(pdf_path).resolve() if pdf_path is not None else None
    source_root = Path(source_root or DEFAULT_SOURCE_ROOT).resolve()
    output_root = Path(output_root or DEFAULT_OUTPUT_ROOT).resolve()
    if source_root == output_root or source_root in output_root.parents or output_root in source_root.parents:
        raise ValueError('Thư mục giáo án gốc và đầu ra phải tách biệt.')
    filename = None
    if pdf_path is not None:
        filename = (original_filename or pdf_path.name).replace('\\', '/').split('/')[-1]
        if Path(filename).suffix.lower() != '.pdf' or not pdf_path.is_file():
            raise ValueError('PDF đã chọn không tồn tại hoặc không đúng định dạng.')
        with pdf_path.open('rb') as stream:
            if b'%PDF-' not in stream.read(1024):
                raise ValueError('File không có header PDF hợp lệ.')
    elif not source_subject or not source_series:
        raise ValueError('Chọn môn học và bộ sách khi không tải PDF.')
    if batch_size < 1:
        raise ValueError('batch_size phải > 0.')
    job_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '_' + uuid.uuid4().hex[:12]
    job_dir = output_root / 'jobs' / job_id
    job_dir.mkdir(parents=True)
    report_path = job_dir / 'report.json'
    pdf_hash = None
    if pdf_path is not None:
        digest = hashlib.sha256()
        with pdf_path.open('rb') as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b''):
                digest.update(block)
        pdf_hash = digest.hexdigest()
    report = {'job_id': job_id, 'uploaded_filename': filename, 'uploaded_pdf_path': str(pdf_path) if pdf_path else None,
              'pdf_sha256': pdf_hash, 'pdf_extracted': False, 'source_mode': 'prepared_markdown',
              'book_name': name, 'lesson_plan_name': name, 'lesson_plan_id': lesson_plan_id,
              'target_collection': DEFAULT_COLLECTION_NAME, 'report_path': str(report_path),
              'warnings': [], 'status': 'created'}
    def save(status):
        report['status'] = status
        temp = report_path.with_suffix('.tmp')
        temp.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
        temp.replace(report_path)
        logger.info('AUTO_INDEXING job=%s status=%s collection=%s', job_id, status, report['target_collection'])
        if on_progress:
            on_progress({'stage': status, 'job_id': job_id, 'total_chunks': report.get('total_chunks')})
    try:
        save('selecting_prepared_markdown')
        # UI fields select the prepared data. PDF bytes never feed the chunker.
        hint = f'{source_subject} 10 {source_series or ""}.pdf' if source_subject else filename
        try:
            subject, series, files = select_sources(hint, source_root)
        except ValueError:
            if source_subject:
                raise
            subject, series, files = select_sources(name + '.pdf', source_root)
        if any(not path.is_relative_to(source_root) for path in files):
            raise ValueError('Markdown gốc nằm ngoài source_root.')
        from src.modules.rag.process_toan_10.push_giao_an_qdrant import build_all_chunks, point_id
        save('chunking_prepared_markdown')
        chunks = build_all_chunks(files=files, on_progress=on_progress)
        for chunk in chunks:
            chunk['metadata'] = {**chunk['metadata'], 'lesson_plan_name': name, 'lesson_plan_id': lesson_plan_id}
        ids = [point_id(chunk) for chunk in chunks]
        if not chunks or len(ids) != len(set(ids)):
            raise ValueError('Không có chunks hoặc bị trùng chunk ID.')
        chunks_path = job_dir / 'prepared_chunks.json'
        chunks_path.write_text(json.dumps(chunks, ensure_ascii=False, indent=2), encoding='utf-8')
        report.update(subject=subject, textbook_series=series, total_chunks=len(chunks),
                      indexing_source_files=[str(path) for path in files], prepared_chunks_path=str(chunks_path))
        if upload:
            save('checking_qdrant_config')
            from .collections import validate_qdrant_configuration, upload_to_default_collection
            _, _, destination = validate_qdrant_configuration()
            report['target_collection'] = destination
            save('preparing_index')
            report['qdrant'] = upload_to_default_collection(chunks, batch_size=batch_size, on_progress=on_progress)
            save('completed')
        else:
            save('preview_ready')
        return report
    except Exception as exc:
        failed_stage = report['status']
        report.update(error=str(exc), failed_stage=failed_stage,
                      qdrant_may_be_partial=failed_stage in ('preparing_index', 'uploading_prepared_markdown'))
        save('failed')
        raise AutoIndexingError(str(exc), report_path, 422) from exc
