from fastapi import APIRouter

from pydantic import BaseModel

router = APIRouter()

@router.get("/user/")
async def get_user():
    return {"response": "endpoint user"}



def init_app(app):
    app.include_router(router)