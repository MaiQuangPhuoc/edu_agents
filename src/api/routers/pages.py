from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@router.get("/exam/{exam_id}/take")
def exam_page(request: Request, exam_id: str):
    return templates.TemplateResponse("exam.html", {"request": request, "exam_id": exam_id})