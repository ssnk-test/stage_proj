from fastapi import FastAPI
from email_service.models import db
import logging
from importlib.metadata import entry_points

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





