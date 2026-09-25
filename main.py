from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.api.routers import router as api_router
from backend.web.web import router as web_router
from backend.optimizer_v01.cash_creator import initialize_optimizer_cash

PATH_TO_STATIC = "frontend/static"

@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_optimizer_cash()
    yield

app = FastAPI(title="My Great Project", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="./frontend/static"), name="static")

app.include_router(api_router)
app.include_router(web_router)
