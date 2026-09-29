import datetime
import json

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.api.routers import get_optimizer_results, get_requests, get_engineers

router = APIRouter(tags=["Frontend Pages"])
# !!!ВАЖНО: внизу дириктория отсчитывается не от web.py, а от main.py
templates = Jinja2Templates(directory="frontend/templates")


@router.get("/index", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    def find_engineer(engineer_id: int, engineers):
        for engineer in engineers:
            if engineer["id"] == engineer_id:
                return engineer
        return None

    vehicle_dict = {
        "car": "автомобиль",
        "on_foot": "пешком",
        "bicycle": "велосипед",
        "public_transport": "общественный транспорт",
    }

    optimizer_json = (await get_optimizer_results())['data']
    engineers_json = json.loads((await get_engineers())['data'])
    requests_json = json.loads((await get_requests())['data'])

    return templates.TemplateResponse(name="index.html", request=request, context={
        "JSON": optimizer_json,
        "engineers": engineers_json,
        "requests": requests_json,
        "find_engineer": find_engineer,
        "vehicles": vehicle_dict
    })


@router.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    return templates.TemplateResponse(name="admin.html", request=request)
