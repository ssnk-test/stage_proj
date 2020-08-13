from .main import get_app
from ..cel.celer import app as app_cel
import asyncio
app = get_app()





#async def strt(loop):

# celery worker -P celery_pool_asyncio:TaskPool -A mon.cel.tasks


#     argv = [
#         'worker',
#         '-P celery_pool_asyncio:TaskPool',
#         '-A mon.tasks'
#
#     ]
#     app_cel.worker_main(argv=argv)
#
# @app.on_event("startup")
# async def startup_event():
#     loop = asyncio.get_event_loop()
#     asyncio.create_task(strt(loop))
