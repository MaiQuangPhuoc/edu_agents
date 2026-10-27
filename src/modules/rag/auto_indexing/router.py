"""Optional FastAPI adapter. Mount this router in the existing application."""

import asyncio
import logging
import uuid
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from starlette.concurrency import run_in_threadpool

from .pipeline import AutoIndexingError, run_auto_indexing
from .sources import DEFAULT_OUTPUT_ROOT

router = APIRouter(prefix="/auto-indexing", tags=["auto-indexing"])
logger = logging.getLogger(__name__)
MAX_UPLOAD_BYTES = 30 * 1024 * 1024
_processing_slot = asyncio.Semaphore(1)


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...), book_name: str = Form(...)):
    return await process_pdf_upload(file, book_name=book_name)


async def process_pdf_upload(file: UploadFile, *, book_name, source_subject=None, source_series=None):
    """Store one PDF for viewing, then index prepared Markdown under book_name.

    Source/output roots and collection are server configuration, not fields a
    browser may submit. A random saved name cannot change subject detection.
    """
    filename = (file.filename or "").replace("\\", "/").split("/")[-1]
    if Path(filename).suffix.casefold() != ".pdf":
        await file.close()
        raise HTTPException(400, "Chỉ nhận file PDF.")
    upload_dir = DEFAULT_OUTPUT_ROOT / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)
    path = upload_dir / f"{uuid.uuid4().hex}.pdf"
    try:
        size = 0
        with path.open("xb") as target:
            while block := await file.read(1024 * 1024):
                size += len(block)
                if size > MAX_UPLOAD_BYTES:
                    raise HTTPException(413, "PDF vượt giới hạn 30 MB.")
                # Keep disk writes off the event loop, as well as extraction/embedding.
                await run_in_threadpool(target.write, block)
        # One indexing job per API worker avoids loading competing CPU models.
        async with _processing_slot:
            return await run_in_threadpool(run_auto_indexing, path, book_name=book_name, original_filename=filename,
                                                source_subject=source_subject, source_series=source_series)
    except HTTPException:
        path.unlink(missing_ok=True)
        raise
    except (ValueError, FileNotFoundError) as exc:
        path.unlink(missing_ok=True)
        raise HTTPException(400, str(exc)) from exc
    except AutoIndexingError as exc:
        logger.exception("Auto indexing failed; report=%s", exc.report_path)
        raise HTTPException(exc.status_code, {"message": str(exc), "report_path": str(exc.report_path)}) from exc
    finally:
        await file.close()
