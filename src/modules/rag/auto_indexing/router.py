"""PDF upload and optional live server-sent progress for the existing UI."""
import asyncio
import json
import logging
import uuid
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from starlette.concurrency import run_in_threadpool

from .pipeline import AutoIndexingError, run_auto_indexing
from .sources import DEFAULT_OUTPUT_ROOT

router = APIRouter(prefix='/auto-indexing', tags=['auto-indexing'])
logger = logging.getLogger(__name__)
MAX_UPLOAD_BYTES = 30 * 1024 * 1024
_processing_slot = asyncio.Semaphore(1)
_stream_jobs = set()


async def save_pdf_upload(file):
    filename = (file.filename or '').replace('\\', '/').split('/')[-1]
    if Path(filename).suffix.lower() != '.pdf':
        await file.close()
        raise HTTPException(400, 'Chỉ nhận file PDF.')
    upload_dir = DEFAULT_OUTPUT_ROOT / 'uploads'
    upload_dir.mkdir(parents=True, exist_ok=True)
    path = upload_dir / f'{uuid.uuid4().hex}.pdf'
    try:
        size = 0
        with path.open('xb') as target:
            while block := await file.read(1024 * 1024):
                size += len(block)
                if size > MAX_UPLOAD_BYTES:
                    raise HTTPException(413, 'PDF vượt giới hạn 30 MB.')
                await run_in_threadpool(target.write, block)
        return path, filename
    except Exception:
        path.unlink(missing_ok=True)
        raise
    finally:
        await file.close()


def indexing_http_error(exc):
    if isinstance(exc, AutoIndexingError):
        return HTTPException(exc.status_code, {'message': str(exc), 'report_path': str(exc.report_path)})
    return HTTPException(400, str(exc))


@router.post('/upload')
async def upload_pdf(file: UploadFile = File(...), book_name: str = Form(...)):
    return await process_pdf_upload(file, book_name=book_name)


async def process_pdf_upload(file, *, book_name, source_subject=None, source_series=None):
    path, filename = await save_pdf_upload(file) if file is not None else (None, None)
    try:
        async with _processing_slot:
            return await run_in_threadpool(run_auto_indexing, path, book_name=book_name,
                original_filename=filename, source_subject=source_subject, source_series=source_series)
    except (AutoIndexingError, ValueError, FileNotFoundError) as exc:
        raise indexing_http_error(exc) from exc


async def stream_pdf_upload(file, *, book_name, complete, source_subject=None, source_series=None):
    # Persist/close UploadFile BEFORE returning a StreamingResponse. This also
    # works with FastAPI versions that close request files when the route returns.
    path, filename = await save_pdf_upload(file) if file is not None else (None, None)
    loop = asyncio.get_running_loop()
    queue = asyncio.Queue(maxsize=256)

    def deliver(event):
        if queue.full():
            queue.get_nowait()
        queue.put_nowait(event)

    def progress(event):
        event = dict(event)
        # Indexing is done, but the book record still needs to be saved.
        if event.get('stage') == 'completed':
            event['stage'] = 'saving_document'
        if not loop.is_closed():
            try:
                loop.call_soon_threadsafe(deliver, {'type': 'progress', **event})
            except RuntimeError:
                pass  # Display transport must not interrupt an indexing operation.

    async def worker():
        try:
            progress({'stage': 'file_saved', 'message': f'Đã lưu PDF: {filename}.' if filename else 'Đã nhận môn học và bộ sách; sử dụng giáo án có sẵn, không cần PDF.'})
            if _processing_slot.locked():
                progress({'stage': 'queued', 'message': 'Đang chờ lượt xử lý trên máy chủ.'})
            async with _processing_slot:
                result = await run_in_threadpool(run_auto_indexing, path, book_name=book_name,
                    original_filename=filename, source_subject=source_subject,
                    source_series=source_series, on_progress=progress)
                if result.get('status') != 'completed':
                    raise RuntimeError('Indexing chưa hoàn thành.')
                progress({'stage': 'saving_document', 'message': 'Đang lưu thông tin sách và kết quả indexing.'})
                document = await run_in_threadpool(complete, result)
            deliver({'type': 'result', 'document': document})
        except Exception as exc:
            logger.exception('Indexing stream failed: %s', filename)
            message = str(exc)
            status_code = getattr(exc, 'status_code', 500)
            if isinstance(exc, HTTPException):
                message = exc.detail if isinstance(exc.detail, str) else exc.detail.get('message', str(exc.detail))
            deliver({'type': 'error', 'message': message, 'status_code': status_code})

    async def events():
        task = asyncio.create_task(worker())
        # Keep a strong reference: if the browser disconnects the current upload
        # still finishes and saves its book record, rather than becoming orphaned.
        _stream_jobs.add(task)
        task.add_done_callback(_stream_jobs.discard)
        while True:
            try:
                event = await asyncio.wait_for(queue.get(), timeout=10)
            except asyncio.TimeoutError:
                yield ': keep-alive\n\n'
                continue
            yield 'data: ' + json.dumps(event, ensure_ascii=False) + '\n\n'
            if event['type'] in ('result', 'error'):
                break

    return StreamingResponse(events(), media_type='text/event-stream', headers={
        'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})
