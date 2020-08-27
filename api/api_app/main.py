from fastapi import FastAPI
from api_app.views.endpoints import router


def get_app():
    app = FastAPI(title="API service")
    app.include_router(router)

    return app
