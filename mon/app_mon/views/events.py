from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app_mon.models.event import Event
from cel.tasks import write_event


router = APIRouter()


@router.get("/events")
async def get_events():

    ev = await Event.query.gino.all()
    resp = []
    for item in ev:
        resp.append(
            {"service": item.service,
             "url": item.url,
             "status": item.status,
             "req_time": item.req_time,
             "res_time": item.res_time
             })
    return resp


class EventModel(BaseModel):
    service: str
    url: str
    status: str
    req_time: str
    res_time: str


@router.post("/events")
async def add_event(ev: EventModel):
    await write_event(service=ev.service,
                      url=ev.url,
                      status=ev.status,
                      dt1=ev.req_time,
                      dt2=ev.res_time)

    return {"resp": "ok"}


def init_app(app):
    app.include_router(router)