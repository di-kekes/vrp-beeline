from fastapi import FastAPI
# Импортируем роутер из файла с логикой
from api.routers import router

app = FastAPI(title="My Great Project")

# Подключаем роутер к главному приложению
app.include_router(router)

