"""Register book metadata or upload a PDF and run prepared-Markdown indexing."""
import json
import re
import threading
import uuid
from pathlib import Path
from fastapi import APIRouter, HTTPException, File, Form, UploadFile
from pydantic import BaseModel, Field
from starlette.concurrency import run_in_threadpool
from fastapi.responses import FileResponse
from src.modules.rag.auto_indexing.sources import DEFAULT_OUTPUT_ROOT
from src.modules.rag.auto_indexing.name_registry import validate_name

from src.modules.rag.auto_indexing.router import process_pdf_upload
from src.modules.rag.auto_indexing.sources import SUBJECTS as INDEXING_SUBJECTS

router = APIRouter(prefix='/api/ui/books', tags=['books'])
DATA = Path(__file__).resolve().parents[2] / 'data' / 'edu_ui_books'
LOCK = threading.RLock()
UPLOAD_ROOT = DEFAULT_OUTPUT_ROOT / 'uploads'
SERIES = ['ket_noi', 'chan_troi', 'canh_dieu', 'khac']
SUBJECTS = ['Toán', 'Ngữ văn', 'Tiếng Anh', 'Vật lí', 'Hóa học', 'Sinh học',
            'Lịch sử', 'Địa lí', 'Giáo dục kinh tế và pháp luật', 'Tin học',
            'Công nghệ', 'Giáo dục quốc phòng và an ninh', 'Giáo dục thể chất',
            'Âm nhạc', 'Mĩ thuật', 'Hoạt động trải nghiệm, hướng nghiệp', 'Khác']
# Only demonstrative catalog entries: they are NOT verified sources or RAG-indexed books.
CATALOG = [dict(book_id=f'{series}_{i}', series=series, subject=subject,
                title=f'{subject} 10', grade=10, rag_ready=False, cover_url=None)
           for series in SERIES[:3] for i, subject in enumerate(SUBJECTS[:-1], 1)]
INDEXING_SERIES_TO_UI = {'chan_troi_sang_tao': 'chan_troi',
                         'ket_noi_tri_thuc': 'ket_noi', 'canh_dieu': 'canh_dieu'}

class AttachBook(BaseModel):
    student_id: str = Field(min_length=1, max_length=80)
    book_id: str | None = None
    title: str = Field(min_length=1, max_length=200)
    series: str
    subject: str
    display_name: str = Field(min_length=1, max_length=150)
    description: str = Field(default='', max_length=1000)

def storage(student_id: str) -> Path:
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,80}', student_id):
        raise HTTPException(422, 'student_id không hợp lệ')
    return DATA / f'{student_id}.json'

def read_items(path: Path):
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(data, list):
            raise ValueError('Invalid JSON')
        return data
    except (ValueError, OSError):
        raise HTTPException(500, 'Không thể đọc danh sách đã lưu')

def write_items(path: Path, items):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding='utf-8')
    temp.replace(path)

@router.get('')
def list_catalog(series: str | None = None, subject: str | None = None):
    return {'books': [b for b in CATALOG if (not series or series == b['series'])
                      and (not subject or subject == b['subject'])]}

@router.get('/mine')
def my_books(student_id: str):
    with LOCK:
        return {'documents': read_items(storage(student_id))}

@router.post('/attach', status_code=201)
def attach_book(body: AttachBook):
    if body.series not in SERIES or body.subject not in SUBJECTS:
        raise HTTPException(422, 'Bộ sách hoặc môn học không hợp lệ')
    title = body.title.strip()
    display_name = body.display_name.strip()
    if not title or not display_name:
        raise HTTPException(422, 'Tên sách và tên tài liệu không được để trống')
    found = next((b for b in CATALOG if b['book_id'] == body.book_id), None)
    if found and (found['series'] != body.series or found['subject'] != body.subject or found['title'] != title):
        raise HTTPException(422, 'Tên sách không khớp danh mục')
    book = found or dict(book_id=str(uuid.uuid4()), title=title, series=body.series,
                         subject=body.subject, grade=10, rag_ready=False, cover_url=None)
    path = storage(body.student_id)
    with LOCK:
        items = read_items(path)
        if any(item['title'].casefold() == title.casefold() and
               item['subject'] == body.subject and item['series'] == body.series for item in items):
            raise HTTPException(409, 'Sách này đã được thêm trước đó')
        item = {**book, 'document_id': str(uuid.uuid4()), 'display_name': display_name,
                'description': body.description.strip()}
        items.append(item)
        write_items(path, items)
    return item


def save_indexed_book(student_id, document_id, display_name, description, result, kind='book'):
    """Only called after indexing succeeded; the PDF-derived result is authoritative."""
    title = result['book_name']
    subject = re.sub(r'\s+10$', '', INDEXING_SUBJECTS[result['subject']][0])
    series = INDEXING_SERIES_TO_UI[result['textbook_series']]
    collection = result['qdrant']['collection_name']
    path = storage(student_id)
    with LOCK:
        items = read_items(path)
        index = next((i for i, item in enumerate(items)
                      if (item.get('document_id') == document_id if document_id else
                          item.get('title') == title and item.get('subject') == subject and item.get('series') == series)), None)
        if document_id and index is None:
            raise HTTPException(404, 'Sách đã bị gỡ trong khi xử lý; collection mới vẫn được giữ.')
        previous = items[index] if index is not None else {}
        item = {
            **previous, 'kind': kind, 'server_saved': True, 'document_id': previous.get('document_id') or str(uuid.uuid4()),
            'book_id': previous.get('book_id') or str(uuid.uuid4()), 'grade': 10,
            'title': title, 'subject': subject, 'series': series,
            'display_name': display_name.strip() or title, 'description': description.strip(),
            'cover_url': None, 'rag_ready': True, 'collection_name': collection,
            'indexing_status': 'completed', 'uploaded_filename': result['uploaded_filename'],
            'uploaded_pdf_path': result['uploaded_pdf_path'],
            'file': {'name': result['uploaded_filename'], 'size': Path(result['uploaded_pdf_path']).stat().st_size, 'type': 'application/pdf'},
            'indexing': {'job_id': result['job_id'], 'report_path': result['report_path'],
                         'total_chunks': result['total_chunks'], 'source_mode': result['source_mode'],
                         'template_collection': result['qdrant']['template_collection']},
        }
        item['file_url'] = f"/api/ui/books/mine/{item['document_id']}/file?student_id={student_id}"
        if index is None:
            items.append(item)
        else:
            items[index] = item
        write_items(path, items)
    return item


@router.post('/upload', status_code=201)
async def upload_and_index_book(file: UploadFile = File(...), student_id: str = Form(...),
                                title: str = Form(..., min_length=1, max_length=200),
                                subject: str | None = Form(None), series: str | None = Form(None),
                                display_name: str = Form('', max_length=150),
                                description: str = Form('', max_length=1000),
                                document_id: str | None = Form(None)):
    # Validate the student/document before costly extraction or collection creation.
    path = storage(student_id)
    if document_id:
        with LOCK:
            if not any(item.get('document_id') == document_id for item in read_items(path)):
                raise HTTPException(404, 'Không thấy tài liệu')
    try:
        name = validate_name(title)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
    source_series = {'chan_troi': 'chan_troi_sang_tao', 'ket_noi': 'ket_noi_tri_thuc', 'canh_dieu': 'canh_dieu'}.get(series)
    result = await process_pdf_upload(file, book_name=name, source_subject=subject, source_series=source_series)
    if result.get('status') != 'completed':
        raise HTTPException(502, 'Indexing chưa hoàn thành; chưa đánh dấu tài liệu sẵn sàng.')
    return await run_in_threadpool(save_indexed_book, student_id, document_id, display_name, description, result)

@router.post('/private/upload', status_code=201)
async def upload_private_pdf(file: UploadFile = File(...), student_id: str = Form(...),
                             name: str = Form(..., min_length=1, max_length=150),
                             subject: str | None = Form(None),
                             description: str = Form('', max_length=1000)):
    storage(student_id)
    try:
        name = validate_name(name)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
    result = await process_pdf_upload(file, book_name=name, source_subject=subject)
    if result.get('status') != 'completed':
        raise HTTPException(502, 'Indexing chưa hoàn thành.')
    return await run_in_threadpool(save_indexed_book, student_id, None, name, description, result, 'private')


@router.get('/mine/{document_id}/file')
def view_uploaded_pdf(document_id: str, student_id: str):
    with LOCK:
        record = next((item for item in read_items(storage(student_id)) if item.get('document_id') == document_id), None)
    if not record or not record.get('uploaded_pdf_path'):
        raise HTTPException(404, 'Chưa có file PDF đã tải lên cho tài liệu này.')
    path = Path(record['uploaded_pdf_path']).resolve()
    if not path.is_relative_to(UPLOAD_ROOT.resolve()) or not path.is_file():
        raise HTTPException(404, 'Không tìm thấy file PDF.')
    return FileResponse(path, media_type='application/pdf', filename=record['uploaded_filename'],
                        content_disposition_type='inline')


@router.put('/mine/{document_id}')
def update_book(document_id: str, body: AttachBook):
    if body.series not in SERIES or body.subject not in SUBJECTS:
        raise HTTPException(422, 'Bộ sách hoặc môn học không hợp lệ')
    title = body.title.strip()
    display_name = body.display_name.strip()
    if not title or not display_name:
        raise HTTPException(422, 'Tên sách và tên tài liệu không được để trống')
    found = next((b for b in CATALOG if b['book_id'] == body.book_id), None)
    if found and (found['series'] != body.series or found['subject'] != body.subject or found['title'] != title):
        raise HTTPException(422, 'Tên sách không khớp danh mục')

    path = storage(body.student_id)
    with LOCK:
        items = read_items(path)
        index = next(
            (i for i, item in enumerate(items) if item.get('document_id') == document_id),
            None,
        )
        if index is None:
            raise HTTPException(404, 'Không thấy tài liệu')
        if any(
            i != index
            and item['title'].casefold() == title.casefold()
            and item['subject'] == body.subject
            and item['series'] == body.series
            for i, item in enumerate(items)
        ):
            raise HTTPException(409, 'Sách này đã được thêm trước đó')

        previous = items[index]
        book = found or {
            'book_id': previous.get('book_id', str(uuid.uuid4())),
            'title': title,
            'series': body.series,
            'subject': body.subject,
            'grade': previous.get('grade', 10),
            'rag_ready': previous.get('rag_ready', False),
            'cover_url': previous.get('cover_url'),
        }
        same_identity = (previous.get('title') == title and previous.get('subject') == body.subject
                         and previous.get('series') == body.series)
        updated = {
            **previous, **book,
            'document_id': document_id,
            'display_name': display_name,
            'description': body.description.strip(),
        }
        if same_identity:
            updated['rag_ready'] = previous.get('rag_ready', False)
        else:
            updated['rag_ready'] = False
            for key in ('collection_name', 'indexing', 'uploaded_filename', 'indexing_status'):
                updated.pop(key, None)
        items[index] = updated
        write_items(path, items)
    return updated

@router.delete('/mine/{document_id}')
def delete_book(document_id: str, student_id: str):
    path = storage(student_id)
    with LOCK:
        items = read_items(path)
        updated = [item for item in items if item.get('document_id') != document_id]
        if len(items) == len(updated):
            raise HTTPException(404, 'Không thấy tài liệu')
        write_items(path, updated)
    return {'removed': True}

