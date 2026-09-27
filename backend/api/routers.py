from pydantic import TypeAdapter
from fastapi import APIRouter
from data import sintetic_dataset
import data.json_bd as db

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
    eng = db.get_engineer_by_id(id)
    try:
        data = db.delete_engineer(eng)
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