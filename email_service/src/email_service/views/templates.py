from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import json
import aio_pika
from email_service.models.templates import Templates

router = APIRouter()


@router.get("/templates")
async def get_template():
    templates = await Templates.query.gino.all()
    resp = {}
    for item in templates:
        resp[item.name] = item.body
    return resp


class TemplatesModel(BaseModel):
    name: str
    body: str


@router.post("/templates")
async def add_template(body: TemplatesModel):
    r = await Templates.create(name=body.name, body=body.body)
    return {"response": "ok"}


def init_app(app):
    app.include_router(router)




