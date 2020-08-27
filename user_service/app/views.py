from aiohttp import web
from datetime import datetime, timedelta
import sqlalchemy as sa
import argon2 as argon
from .model import Users
from jose import jwt
import jose
from functools import wraps
import uuid
from config import settings


def auth(f):
    @wraps(f)
    async def wrapper(*args, **kwds):

        inst = args[0]

        # get access token
        header_auth = inst.request.headers["Authorization"]

        if header_auth.startswith("Bearer"):
            access_token = header_auth.split(" ")[1]
        else:
            return web.json_response({"response": "no auth"})

        # unpack JWT
        try:
            access_token_jwt = jwt.decode(
                access_token,
                settings.jwt_phrase
            )
        except jose.exceptions.JWTError:
            return web.json_response({"response": "invalid auth token"})

        # get access token from redis
        redis = await inst.request.app["redis_pool"]

        if not await redis.exists(access_token_jwt["uuid"]):
            return web.json_response({"response": "invalid auth token"})

        redis_row = await redis.get(access_token_jwt["uuid"])
        access_token_redis = redis_row.decode("utf-8").split(" ")[0]

        if access_token != access_token_redis:
            return web.json_response({"response": "invalid auth token"})

        return await f(*args, access_token_jwt, **kwds)

    return wrapper


class RegView(web.View):

    async def post(self):
        body_dict = await self.request.json()
        if "username" not in body_dict \
                or "password" not in body_dict \
                or "email" not in body_dict:
            return web.json_response({"resp": "reg user fail"})

        ph = argon.PasswordHasher()
        password = ph.hash(body_dict["password"])

        body_dict['uuid'] = str(uuid.uuid4())
        body_dict['password'] = password

        async with self.request.app["database_pool"].acquire() as conn:
            await conn.execute(sa.insert(Users).values(**body_dict))

        return web.json_response({"resp": f"add user {body_dict['username']}"})


class LogInView(web.View):

    async def post(self):
        body_dict = await self.request.json()

        async with self.request.app["database_pool"].acquire() as conn:
            user = await conn.fetchrow(
                sa.select([Users]).where(Users.username == body_dict['username']))

        if user is not None:
            pass_crypt = user["password"]
            ph = argon.PasswordHasher()

            try:
                ph.verify(pass_crypt, body_dict["password"])
            except argon.exceptions.VerifyMismatchError:
                return web.json_response({"resp": "wrong password"})

            a_token = jwt.encode(
                {
                    "username": body_dict['username'],
                    "exp": datetime.now() + timedelta(minutes=15),
                    "uuid": user["uuid"]
                },
                settings.jwt_phrase)
            r_token = jwt.encode(
                {
                    "username": body_dict['username'],
                    "exp": datetime.now() + timedelta(minutes=40),
                    "uuid": user["uuid"]
                },
                settings.jwt_phrase)

            redis = self.request.app["redis_pool"]
            await redis.set(user["uuid"], " ".join([a_token, r_token]))
            await redis.expire(user["uuid"], 60 * 40)

            return web.json_response({"atoken": a_token, "rtoken": r_token})

        return web.json_response({"resp": "login fail"})


class LogOutView(web.View):
    @auth
    async def post(self, access_token_jwt):
        redis = await self.request.app["redis_pool"]
        await redis.delete(access_token_jwt["uuid"])
        return web.json_response({"resp": "ok"})


class UpdateView(web.View):
    @auth
    async def post(self, access_token_jwt):
        body_dict = await self.request.json()
        username = access_token_jwt["username"]
        pool = self.request.app["database_pool"]
        a = body_dict
        body_dict = dict()
        for item in a.keys():
            if a[item] is not None:
                body_dict[item] = a[item]
        # gen password hash
        if "password" in body_dict:
            ph = argon.PasswordHasher()
            password = ph.hash(body_dict["password"])
            body_dict["password"] = password

        # update user info
        async with pool.acquire() as conn:
            query = sa.update(Users).where(Users.username == username).values(**body_dict)
            await conn.execute(query)
        return web.json_response({"resp": "update ok"})


class InfoView(web.View):
    @auth
    async def get(self, access_token_jwt):
        pool = self.request.app["database_pool"]
        username = access_token_jwt["username"]
        async with pool.acquire() as conn:
            resp = await conn.fetchrow(
                sa.select([Users]).where(Users.username == username))
        return web.json_response({"response": "ok", "username": resp['username'],
                                  "email": resp['email'], 'uuid': resp['uuid']})


class RefreshView(web.View):
    async def post(self):
        body_dict = await self.request.json()
        redis = await self.request.app["redis_pool"]

        try:
            r_token = body_dict['rtoken']
        except KeyError:
            return web.json_response({"response": "no refresh token"})

        # get access token
        header_auth = self.request.headers["Authorization"]

        if "Bearer" in header_auth:
            a_token = header_auth.split(" ")[1]
        else:
            return web.json_response({"response": "no auth"})

        # unpack refresh JWT
        try:
            r_token_jwt = jwt.decode(
                r_token,
                settings.jwt_phrase
            )
        except jose.exceptions.JWTError:
            return web.json_response({"response": "invalid auth token"})

        # get tokens from redis
        user_uuid = r_token_jwt["uuid"]
        if not await redis.exists(user_uuid):
            return web.json_response({"response": "invalid auth,refresh tokens"})
        redis_row = await redis.get(user_uuid)
        a_token_redis, r_token_redis = redis_row.decode("utf-8").split(" ")

        # validate
        if r_token_redis != r_token and a_token_redis != a_token:
            return web.json_response({"response": "invalid auth,refresh tokens"})

        # maybe hack? delete tokens
        if (r_token_redis != r_token) != (a_token_redis != a_token):
            await redis.delete(user_uuid)
            return web.json_response({"response": "invalid auth,refresh tokens"})

        # create new tokens
        a_token = jwt.encode(
            {
                "username": r_token_jwt['username'],
                "exp": datetime.now() + timedelta(minutes=15),
                "uuid": user_uuid
            },
            settings.jwt_phrase)
        r_token = jwt.encode(
            {
                "username": r_token_jwt['username'],
                "exp": datetime.now() + timedelta(minutes=40),
                "uuid": user_uuid
            },
            settings.jwt_phrase)

        await redis.set(user_uuid, " ".join([a_token, r_token]))
        await redis.expire(user_uuid, 60 * 40)

        return web.json_response({"atoken": a_token, "rtoken": r_token})
