from fastapi import FastAPI
from backend.api.routers import router as api_router
from backend.web.web import router as web_router
from fastapi.staticfiles import StaticFiles
#здесь переменные templates и статик
PATH_TO_STATIC = "frontend/static"

app = FastAPI(title="My Great Project")

app.mount("/static", StaticFiles(directory="./frontend/static"), name="static")
# Подключаем роутеры
app.include_router(api_router)
app.include_router(web_router)
