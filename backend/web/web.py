from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

PATH_TO_TEMPLATES = "../frontend/templates"

router = APIRouter(tags=["Frontend Pages"])

templates = Jinja2Templates(directory=PATH_TO_TEMPLATES)

@router.get("/index",response_class=HTMLResponse)
@router.get("/",response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse(name="index.html", request=request)

@router.get("/admin",response_class=HTMLResponse)
async def admin(request: Request):
    return templates.TemplateResponse(name="admin.html", request=request)