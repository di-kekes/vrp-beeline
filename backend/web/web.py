from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from requests import get
import json

router = APIRouter(tags=["Frontend Pages"])
#!!!ВАЖНО: внизу дириктория отсчитывается не от web.py, а от main.py
templates = Jinja2Templates(directory="frontend/templates")
@router.get("/index",response_class=HTMLResponse)
@router.get("/",response_class=HTMLResponse)
def root(request: Request):
    response = get("http://localhost:8000/api/get_engineers")
    engineers_json = json.loads(response.json()['data'])
    return templates.TemplateResponse(name="index.html", request=request, context={"JSON": engineers_json})

@router.get("/admin",response_class=HTMLResponse)
async def admin(request: Request):
    return templates.TemplateResponse(name="admin.html", request=request)