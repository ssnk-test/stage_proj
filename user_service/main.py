import logging

from os.path import abspath, dirname, join

from aiohttp import web
from aiohttp_swagger import setup_swagger
import asyncpgsa

import aioredis as aioredis

import aiohttp_session
from aiohttp_session.redis_storage import RedisStorage



# from aiohttp_security import SessionIdentityPolicy
# from aiohttp_security import authorized_userid
# from aiohttp_security import setup as setup_security
# from aiohttp_session import setup as setup_session
# from aiohttp_session.redis_storage import RedisStorage
# import aioredis
# from aiohttpdemo_blog.db_auth import DBAuthorizationPolicy
# from aiohttpdemo_blog.db import init_db
from app.routes import setup_routes
# from aiohttpdemo_blog.settings import load_config, PACKAGE_NAME



log = logging.getLogger(__name__)


async def setup_redis(app):

    pool = await aioredis.create_redis_pool((
        app['config']['redis']['REDIS_HOST'],
        app['config']['redis']['REDIS_PORT']
    ))

    async def close_redis(app):
        pool.close()
        await pool.wait_closed()

    app.on_cleanup.append(close_redis)
    app['redis_pool'] = pool
    return pool



async def init_app(config):

    app = web.Application()

    #app['config'] = config




    pool = await asyncpgsa.create_pool(
        dsn="postgresql://postgres:postgres@db_user_service:5432/postgres")

    app["database_pool"] = pool

    redis_pool = await aioredis.create_redis_pool(("redis_db", 6379))

    app["redis_pool"] = redis_pool

    aiohttp_session.setup(app, RedisStorage(redis_pool))


    setup_routes(app)
    swwager_file_path = abspath(join(dirname(__file__), "app/swagger.yaml"))
    setup_swagger(app, swagger_url="/swagger",
                  swagger_from_file=swwager_file_path)




    #db_pool = await init_db(app)

    #redis_pool = await setup_redis(app)
    #setup_session(app, RedisStorage(redis_pool))


    #log.debug(app['config'])

    return app


def main(configpath):
    #config = load_config(configpath)
    #logging.basicConfig(level=logging.DEBUG)
    #app = init_app(config)
    app = init_app(None)
    web.run_app(app)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Provide path to config file")
    args = parser.parse_args()

    if args.config:
        main(args.config)
    else:
        main(None)