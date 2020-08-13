#! /bin/bash

uvicorn --host 0.0.0.0 --port 8082 mon.app_mon.asgi:app --reload &

celery worker -P celery_pool_asyncio:TaskPool -A mon.cel.tasks