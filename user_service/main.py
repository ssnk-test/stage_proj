from os.path import abspath, dirname, join
from aiohttp import web
from aiohttp_swagger import setup_swagger
import asyncpgsa
import aioredis as aioredis
from app.routes import setup_routes
from config import settings

async def init_app():
    app = web.Application()

    # db
    db_pool = await asyncpgsa.create_pool(
        dsn=settings.db_dsn)
    app["database_pool"] = db_pool

    # redis
    redis_pool = await aioredis.create_redis_pool(("redis_db", 6379))
    app["redis_pool"] = redis_pool

    # endpoints
    setup_routes(app)

    # swagger
    swwager_file_path = abspath(join(dirname(__file__), "app/swagger.yaml"))
    setup_swagger(
        app,
        swagger_url="/swagger",
        swagger_from_file=swwager_file_path)

    return app


def main():
    print(settings.db_dsn)
    app = init_app()
    web.run_app(app)


if __name__ == '__main__':
    main()
