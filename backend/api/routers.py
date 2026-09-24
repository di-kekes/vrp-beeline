from pydantic import TypeAdapter
from fastapi import APIRouter
from backend.data import sintetic_dataset
import backend.data.json_bd as db
from backend.optimizer_v01.vrp_optimazer import optimize_vrptw
import backend.data.data_schemas as schemas
import backend.optimizer_v01.time_matrix as time
from backend.optimizer_v01.vrp_optimazer import OptimizationResult
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
    try:
        requests = db.get_all_requests()
        engineers = db.get_all_engineers()
        # 0 — депо, 1 и 2 — заявки
        positions = [(i.location.latitude, i.location.longitude) for i in requests]
        depot_location = schemas.Location(
            latitude=engineers[0].start_location.latitude,
            longitude=engineers[0].start_location.longitude,
        )
        positions = [(depot_location.latitude, depot_location.longitude)] + positions
        time_matrix = await time.build_time_matrix(positions)
        result = optimize_vrptw(
            requests=requests,
            engineers=engineers,
            time_matrix=time_matrix,
            depot_location=depot_location,
            solver_time_limit_seconds=30,
            )
        type_adapter = TypeAdapter(OptimizationResult)
        data = type_adapter.dump_json(result)
        return {"code":200, "data":data}
    except Exception as e:
        return e

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
async def delete_request(request: db.Request):
    try:
        data = db.delete_request(request.id)
        return {"code": 200,"data":data}
    except Exception as e:
        return {"code": 500, "message": str(e),}
@router.delete("/engineer_unavailable")
async def engineer_unavailable(engineer: db.Engineer):
    try:
        data = db.delete_engineer(engineer.id )
        return {"code": 200,"data":data,"database":...}
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