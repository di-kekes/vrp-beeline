from fastapi import APIRouter

import data.json_bd as db
router = APIRouter(
    prefix="/api",
    tags=["All api by now"]
)
# апишка

@router.post("/urgent_request")
async def urgent_request(request: db.Request):
    try:
        data = db.create_request(request)
        return {"code": 200}
    except Exception as e:
        return {"code":400, "message":str(e)}

@router.delete("/delete_request")
async def delete_request(request: db.Request):
    try:
        data = db.delete_request(request.id)
        return {"code": 200}
    except Exception as e:
        return {"code": 400, "message": str(e)}
@router.put("/engineer_unavailable")
async def engineer_unavailable(engineer: db.Engineer):
    try:
        data = db.engineer_unavailable(engineer.id)
        return {"code": 200}
    except Exception as e:
        return {"code": 400, "message": str(e)}