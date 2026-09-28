from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.api.routers import get_optimizer_results, get_requests, get_engineers
from requests import get
import json

router = APIRouter(tags=["Frontend Pages"])
# !!!ВАЖНО: внизу дириктория отсчитывается не от web.py, а от main.py
templates = Jinja2Templates(directory="frontend/templates")


@router.get("/index", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    engineers_json = (await get_engineers())['data']
    optimizer_json = (await get_optimizer_results())['data']
    requests_json = (await get_requests())['data']

    return templates.TemplateResponse(name="index.html", request=request, context={
        "JSON": optimizer_json,
        "engineers": engineers_json,
        "requests": requests_json
    })


@router.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    return templates.TemplateResponse(name="admin.html", request=request)
