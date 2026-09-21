from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

PATH_TO_TEMPLATES = "../frontend/templates"

router = APIRouter(tags=["Frontend Pages"])

templates = Jinja2Templates(directory=PATH_TO_TEMPLATES)

@router.get("/index",response_class=HTMLResponse)
@router.get("/",response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse(name="index.html", request=request, context={"JSON": JSON_FROM_BACKEND})

@router.get("/admin",response_class=HTMLResponse)
async def admin(request: Request):
    return templates.TemplateResponse(name="admin.html", request=request)


JSON_FROM_BACKEND = [
    {
        "id": 1,
        "name": "Иван Сидоров",
        "start_location": {
            "latitude": 55.7558,
            "longitude": 37.6173,
            "address": "Москва"
        },
        "shift_start": "2026-09-17T09:00:00+03:00",
        "shift_end": "2026-09-17T18:00:00+03:00",
        "skills": [
            "connection_client",
            "accidents_on_tkd"
        ],
        "vehicle_type": "car"
    }
]
