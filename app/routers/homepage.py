from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/", include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse("pages/index.html", {"request": request})
