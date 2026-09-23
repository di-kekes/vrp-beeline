from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from data.json_bd import get_all_engineers
router = APIRouter(tags=["Frontend Pages"])
JSON_FROM_BACKEND = get_all_engineers()
templates = Jinja2Templates(directory="../frontend/templates")
@router.get("/index",response_class=HTMLResponse)
@router.get("/",response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse(name="index.html", request=request, context={"JSON": JSON_FROM_BACKEND})

@router.get("/admin",response_class=HTMLResponse)
async def admin(request: Request):
    return templates.TemplateResponse(name="admin.html", request=request)