"""PDF is stored for viewing; prepared Markdown is the only indexing source."""
import hashlib
import json
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .sources import DEFAULT_OUTPUT_ROOT, DEFAULT_SOURCE_ROOT, select_sources
from .name_registry import DuplicateCollectionName, update_registry, validate_name

logger = logging.getLogger(__name__)


class AutoIndexingError(RuntimeError):
    def __init__(self, message, report_path, status_code=422):
        super().__init__(message)
        self.report_path = report_path
        self.status_code = status_code


def run_auto_indexing(pdf_path, *, book_name, original_filename=None, source_root=None,
                      output_root=None, upload=True, template_collection=None, batch_size=16,
                      source_subject=None, source_series=None, registry_path=None):
    name = validate_name(book_name)
    pdf_path = Path(pdf_path).resolve()
    source_root = Path(source_root or DEFAULT_SOURCE_ROOT).resolve()
    output_root = Path(output_root or DEFAULT_OUTPUT_ROOT).resolve()
    if source_root == output_root or source_root in output_root.parents or output_root in source_root.parents:
        raise ValueError('Thư mục giáo án gốc và đầu ra phải tách biệt.')
    filename = (original_filename or pdf_path.name).replace('\\', '/').split('/')[-1]
    if Path(filename).suffix.lower() != '.pdf' or not pdf_path.is_file():
        raise ValueError('Cần một file PDF có thật để lưu và xem.')
    with pdf_path.open('rb') as stream:
        if b'%PDF-' not in stream.read(1024):
            raise ValueError('File không có header PDF hợp lệ.')
    if batch_size < 1:
        raise ValueError('batch_size phải > 0.')
    job_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '_' + uuid.uuid4().hex[:12]
    job_dir = output_root / 'jobs' / job_id
    job_dir.mkdir(parents=True)
    report_path = job_dir / 'report.json'
    digest = hashlib.sha256()
    with pdf_path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    report = {'job_id': job_id, 'uploaded_filename': filename, 'uploaded_pdf_path': str(pdf_path),
              'pdf_sha256': digest.hexdigest(), 'pdf_extracted': False, 'source_mode': 'prepared_markdown',
              'book_name': name, 'target_collection': name, 'report_path': str(report_path),
              'warnings': [], 'status': 'created'}
    reserved = False
    def save(status):
        report['status'] = status
        temp = report_path.with_suffix('.tmp')
        temp.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
        temp.replace(report_path)
        logger.info('AUTO_INDEXING job=%s status=%s collection=%s', job_id, status, name)
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
        chunks = build_all_chunks(files=files)
        for chunk in chunks:
            chunk['metadata'].update(indexing_source='prepared_markdown', uploaded_pdf_name=filename)
        ids = [point_id(chunk) for chunk in chunks]
        if not chunks or len(ids) != len(set(ids)):
            raise ValueError('Không có chunks hoặc bị trùng chunk ID.')
        chunks_path = job_dir / 'prepared_chunks.json'
        chunks_path.write_text(json.dumps(chunks, ensure_ascii=False, indent=2), encoding='utf-8')
        report.update(subject=subject, textbook_series=series, total_chunks=len(chunks),
                      indexing_source_files=[str(path) for path in files], prepared_chunks_path=str(chunks_path))
        if upload:
            path = update_registry(name, reserve=True, registry_path=registry_path, status='reserved', job_id=job_id)
            reserved = True
            report['collection_registry_path'] = str(path)
            save('creating_collection_and_uploading')
            from .collections import upload_new_collection
            report['qdrant'] = upload_new_collection(chunks, destination=name,
                template_collection=template_collection, batch_size=batch_size)
            update_registry(name, registry_path=registry_path, status='ready', job_id=job_id)
            save('completed')
        else:
            save('preview_ready')
        return report
    except Exception as exc:
        failed_stage = report['status']
        report.update(error=str(exc), failed_stage=failed_stage,
                      qdrant_may_be_partial=failed_stage == 'creating_collection_and_uploading')
        if reserved:
            update_registry(name, registry_path=registry_path, status='failed', job_id=job_id, error=str(exc))
        save('failed')
        raise AutoIndexingError(str(exc), report_path, 409 if isinstance(exc, DuplicateCollectionName) else 422) from exc
