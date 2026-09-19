from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
router = APIRouter(prefix='/',tags=["Frontend Pages"])

templates = Jinja2Templates(directory="../../server/templates")

@router.get("/",response_class=HTMLResponse)
@router.get("/index",response_class=HTMLResponse)
def root():
    return templates.TemplateResponse(name="index.html")

@router.get("/admin",response_class=HTMLResponse)
async def admin():
    return templates.TemplateResponse(name="admin.html")