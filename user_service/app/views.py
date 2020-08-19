# import aiohttp_jinja2
from datetime import datetime
from aiohttp import web
from aiohttp_swagger import swagger_path
import json
from datetime import datetime
import sqlalchemy as sa
from argon2 import PasswordHasher
from .model import Users
from aiohttp_session import get_session, new_session
from jose import jwt
from functools import wraps
import os

import uuid


def auth(f):
    @wraps(f)
    async def  wrapper(*args, **kwds):
        print('Calling decorated function')
        inst = args[0]
        body_dict = await inst.request.json()
        redis = await inst.request.app["redis_pool"]

        try:
            if not await redis.exists(body_dict["atoken"]):
                return web.json_response({"response": "no valid atoken"})
        except:
            return web.json_response({"response": "f'kd body"})

        return await f(*args, **kwds)
    return wrapper


class RegView(web.View):

    async def post(self):
        body_dict = await self.request.json()
        if not "username" in body_dict or \
            not "password" in body_dict or \
            not "email" in body_dict:

            return web.json_response({"code":"400", "resp": "reg user fail"})

        argon2 = PasswordHasher()
        password = argon2.hash(body_dict["password"])

        body_dict['uuid'] = str(uuid.uuid4())
        body_dict['password'] = password

        async with self.request.app["database_pool"].acquire() as conn:
            await conn.execute(sa.insert(Users).values(**body_dict))

        return web.json_response({"code": "201", "resp": f"add user {body_dict['username']}"})


class LogInView(web.View):

    async def post(self):
        body_dict = await self.request.json()

        async with self.request.app["database_pool"].acquire() as conn:
            user = await conn.fetchrow(
                sa.select([Users]).where(Users.username == body_dict['username']))

            if user is not None:
                pass_crypt = user["password"]
                argon2 = PasswordHasher()

                try:
                    argon2.verify(pass_crypt, body_dict["password"])
                except:
                    return web.json_response({"result":"wrong password"})

                a_tocken = jwt.encode(
                    {
                        "user": body_dict['username']
                    },
                    "todo:implement to env")
                r_tocken = jwt.encode(
                    {
                        "user": body_dict['username'],
                        "exp": datetime.now()
                    },
                    "todo:implement to env")


                redis = self.request.app["redis_pool"]
                await redis.set(a_tocken, r_tocken)
                await redis.expire(a_tocken, 120)

                await redis.set(r_tocken, a_tocken)
                await redis.expire(r_tocken, 240)

        return web.json_response({"atoken": a_tocken,"rtoken": r_tocken})


class LogOutView(web.View):
    @auth
    async def post(self):
        print("LogOut valid auth")
        body_dict = await self.request.json()
        redis = await self.request.app["redis_pool"]

        r_tok =  await redis.get(body_dict["atoken"])

        await redis.delete((r_tok).decode("utf-8"))
        await redis.delete(body_dict["atoken"])

        return web.json_response({"response": "ok"})


class UpdateView(web.View):

    @auth
    async def post(self):
        body_dict = await self.request.json()

        # get name from token

        a_tok_param = jwt.decode(
            body_dict["atoken"],
            "todo:implement to env"
            )
        # get user data

        async with self.request.app["database_pool"].acquire() as conn:
            resp = await conn.fetchrow(
                sa.select([Users]).where(Users.username == a_tok_param['user']))

            data_dict = {}
            data_dict[0] = resp[0]
            data_dict[1] = resp[1]
            data_dict[2] = resp[1]

        # udate data
        try:
            data_dict[0] = body_dict["user"]
        except:
            pass

        try:
            data_dict[1] = body_dict["email"]
        except:
            pass

        try:
            argon2 = PasswordHasher()
            password = argon2.hash(body_dict["password"])
            data_dict[2] = password
        except:
            pass

        async with self.request.app["database_pool"].acquire() as conn:
            query = users.update().values(
                username=data_dict[0],
                email=data_dict[1],
                password=data_dict[2]
            )
            await conn.fetchrow(query)

        return web.json_response({"response": "ok"})


class InfoView(web.View):
    @auth
    async def post(self):
        body_dict = await self.request.json()

        a_tok_param = jwt.decode(
            body_dict["atoken"],
            "todo:implement to env"
        )

        async with self.request.app["database_pool"].acquire() as conn:
            resp = await conn.fetchrow(
                sa.select([Users]).where(Users.username == a_tok_param['user']))

        return web.json_response({"response":"ok","username":resp['username'],"email":resp['email']})


class RefreshView(web.View):

    async def post(self):
        body_dict = await self.request.json()
        redis = await self.request.app["redis_pool"]

        if not await redis.exists(body_dict["rtoken"]):
            return web.json_response({"response": "no valid rtoken"})

        r_tok = await redis.get(body_dict["rtoken"])
        a_tok = await redis.get(r_tok.decode("utf-8"))

        # delete
        await redis.delete(r_tok)
        await redis.delete(a_tok)

        # create new tokens

        r_tok_param = jwt.decode(
            r_tok,
            "todo:implement to env"
        )

        a_tocken = jwt.encode(
            {
                "user": r_tok_param["user"]
            },
            "todo:implement to env")
        r_tocken = jwt.encode(
            {
                "user": r_tok_param["user"],
                "exp": datetime.now()
            },
            "todo:implement to env")

        await redis.set(a_tocken, r_tocken)
        await redis.expire(a_tocken, 120)

        await redis.set(r_tocken, a_tocken)
        await redis.expire(r_tocken, 240)

        return web.json_response({"atoken": a_tocken,"rtoken": r_tocken})
