from fastapi import FastAPI
from .models import db
from  .config import config as app_config

from . import config


import logging
import os

from importlib.metadata import entry_points
from email_service.config import config as app_config2


logger = logging.getLogger(__name__)

def load_modules(app=None):
    for ep in entry_points()["email_service.modules"]:
        logger.info("Loading module: %s", ep.name)
        mod = ep.load()
        if app:
            init_app = getattr(mod, "init_app", None)
            if init_app:
                init_app(app)


def get_app():

    app = FastAPI(title="mail_service")
    db.init_app(app)
    load_modules(app)
    return app





