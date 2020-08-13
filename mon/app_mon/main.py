from fastapi import FastAPI

from .models import db
from .views.events import init_app

from . import config
def get_app():
    app = FastAPI(title="events")
    init_app(app)
    db.init_app(app)
    return app