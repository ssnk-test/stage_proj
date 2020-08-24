from fastapi import FastAPI
from email_service.models import db
from email_service.views.templates import router

def get_app():

    app = FastAPI(title="mail_service")
    db.init_app(app)
    app.include_router(router)
    return app







