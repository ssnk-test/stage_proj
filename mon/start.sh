#! /bin/bash
alembic upgrade head &
uvicorn --host 0.0.0.0 --port 8082 app_mon.asgi:app --reload &
celery worker -P celery_pool_asyncio:TaskPool -A cel.tasks