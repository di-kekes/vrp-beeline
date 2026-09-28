from pydantic import TypeAdapter
from fastapi import APIRouter, UploadFile, File

from backend.csv_handler.parse import add_requests_from_csv
from backend.data import sintetic_dataset
import backend.data.json_bd as db
import os, json

import csv

router = APIRouter(
    prefix="/api",
    tags=["All api by now"]
)
# апишка
#GET
@router.get("/get_engineers")
async def get_engineers():
    try:
        type_adapter = TypeAdapter(list[db.Engineer])
        data = type_adapter.dump_json(db.get_all_engineers())
        return {"code":200, "data":data}
    except Exception as e:
        return {"code":500, "error":e}
@router.get("/get_requests")
async def get_requests():
    try:
        type_adapter = TypeAdapter(list[db.Request])
        data = type_adapter.dump_json(db.get_all_requests())
        return {"code":200, "data":data}
    except Exception as e:
        return {"code":500, "error":e}


@router.get("/get_optimizer_results")
async def get_optimizer_results():
    file_path = 'backend/data/data_json/optimizer_cash.json'

    try:
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            return {
                "code": 404,
                "message": "Файл кэша оптимизатора пуст или еще не создан"
            }
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if content == '{}':
                return {
                    "code": 404,
                    "message": "В файле кэша содержится пустой словарь"
                }
            data = json.loads(content)
        return {"code": 200, "data": data}

    except json.JSONDecodeError:
        return {
            "code": 500,
            "message": "Ошибка чтения данных: файл кэша поврежден"
        }
    except Exception as e:
        return {
            "code": 500,
            "message": f"Внутренняя ошибка сервера: {str(e)}"
        }
#POST
@router.post("/add_engineer")
async def add_engineer(engineer: db.Engineer):
    try:
        data = db.create_engineer(engineer)
        return {"code":200, "data":data}
    except Exception as e:
        return {"code":500, "message":str(e)}
@router.post("/urgent_request")
async def urgent_request(request: db.Request):
    try:
        data = db.create_request(request)
        return {"code":200, "data":data}
    except Exception as e:
        return {"code":500, "message":str(e)}

@router.post("/upload_csv")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        return {
            "status_code":400,
            "detail":"Разрешены только CSV-файлы"
        }
    string = await file.read()
    csv_dict = csv.DictReader(string.decode().strip('(').strip(')').splitlines(),delimiter=';')
    add_requests_from_csv(csv_dict)
    return {
        "code":200
    }
#DELETE
@router.delete("/delete_request")
async def delete_request(id:int):
    request = db.get_request_by_id(id)
    try:
        data = db.delete_request(request.id)
        return {"code": 200,"data":data}
    except Exception as e:
        return {"code": 500, "message": str(e),}
@router.delete("/engineer_unavailable")
async def engineer_unavailable(id: int):
    try:
        data = db.delete_engineer(id)
        return {"code": 200,"data":data}
    except Exception as e:
        return {"code": 500, "message": str(e)}
#PUT
@router.put("/generate_dataset")
async def generate_dataset(data=None):
    try:
        sintetic_dataset.start()
        return {"code":200}
    except Exception as e:
        return {"code":500, "error":e}