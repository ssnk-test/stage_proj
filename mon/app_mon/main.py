import sys
sys.path = sys.path[:] + [".."]

from fastapi import FastAPI
from app_mon.models import db
from app_mon.views.events import init_app


def get_app():
    app = FastAPI(title="events")
    init_app(app)
    db.init_app(app)
    return app
