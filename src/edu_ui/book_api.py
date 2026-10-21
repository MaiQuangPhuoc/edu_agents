"""Register book names for a demo student, without uploading files or indexing RAG."""
import json
import re
import threading
import uuid
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix='/api/ui/books', tags=['books'])
DATA = Path(__file__).resolve().parents[2] / 'data' / 'edu_ui_books'
LOCK = threading.RLock()
SERIES = ['ket_noi', 'chan_troi', 'canh_dieu', 'khac']
SUBJECTS = ['Toán', 'Ngữ văn', 'Tiếng Anh', 'Vật lí', 'Hóa học', 'Sinh học',
            'Lịch sử', 'Địa lí', 'Giáo dục kinh tế và pháp luật', 'Tin học',
            'Công nghệ', 'Giáo dục quốc phòng và an ninh', 'Giáo dục thể chất',
            'Âm nhạc', 'Mĩ thuật', 'Hoạt động trải nghiệm, hướng nghiệp', 'Khác']
# Only demonstrative catalog entries: they are NOT verified sources or RAG-indexed books.
CATALOG = [dict(book_id=f'{series}_{i}', series=series, subject=subject,
                title=f'{subject} 10', grade=10, rag_ready=False, cover_url=None)
           for series in SERIES[:3] for i, subject in enumerate(SUBJECTS[:-1], 1)]

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
        updated = {
            **book,
            'document_id': document_id,
            'display_name': display_name,
            'description': body.description.strip(),
        }
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
