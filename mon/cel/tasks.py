from __future__ import absolute_import, unicode_literals

from mon.cel.celer import app
from gino import create_engine
from mon.app_mon.models.event import Event


@app.task(name="tasks.write_event")
async def write_event(service, url, status, dt1, dt2):
    engine = await create_engine("postgresql://postgres:postgres@db_mon_service:5432/postgres")
    await Event.create(
        service=service,
        url=url,
        status=status,
        req_time=dt1,
        res_time=dt2,
        bind=engine)
    await engine.close()
