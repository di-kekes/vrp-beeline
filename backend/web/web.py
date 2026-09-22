from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
router = APIRouter(tags=["Frontend Pages"])

templates = Jinja2Templates(directory="../frontend/templates")
@router.get("/index",response_class=HTMLResponse)
@router.get("/",response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse(name="index.html", request=request, context={"JSON": JSON_FROM_BACKEND})

@router.get("/admin",response_class=HTMLResponse)
async def admin(request: Request):
    return templates.TemplateResponse(name="admin.html", request=request)