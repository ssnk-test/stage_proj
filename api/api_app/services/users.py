from functools import wraps
import asyncio
import httpx
import aio_pika
import aioredis as aioredis
import uuid


class UserServiceAPI:
    def __init__(self):
        self.host = "user_service"
        self.port = "8080"
        self.path = ""

    async def login(self, body):
        url = f"http://{self.host}:{self.port}{self.path}/login"
        async with httpx.AsyncClient() as ac:
            r = await ac.post(url, json=body)
        return r.json()

    async def logout(self, token):
        url = f"http://{self.host}:{self.port}{self.path}/logout"
        headers = {'Authorization': f'Bearer {token.credentials}'}
        async with httpx.AsyncClient() as ac:
            r = await ac.post(url, headers=headers)
        return r.json()

    async def register(self, body):
        """
        body["username"] и body["email"] сигнализируют
        о первойм этапе регистрации

        body["token"] и body["password"] получаем с страницы
        завершения регистрации
        "username" и "email"] не должно быть в запросе

        :param body:
        :return:
        """
        # send email for confrim registration
        if body["username"] is not None and body["email"] is not None:

            # send email for confrim registration
            token = str(uuid.uuid4())
            redis = await aioredis.create_redis_pool(("api_redis", 6379))
            await redis.set(token, ' '.join([body['username'],body['email']]))
            await redis.expire(token, 60 * 15)

            connection = await aio_pika.connect(
                "amqp://test:test@rabbit/", port=5672)
            async with connection:
                routing_key = "send_email"
                channel = await connection.channel()
                headers = {
                    'template': 'html2',
                    'to': body["email"],#"ssnk@le-memese.com",
                    'sub': 'Регистрация',
                    'user': body["username"],
                    'link': f'http://front_endreg/?token={str(token)}'
                }
                await channel.default_exchange.publish(
                    aio_pika.Message(body=b"", headers=headers),
                    routing_key=routing_key,
                )
            return "send email for registration"


        # continue registration after confrim rmail
        if body["token"] is not None and \
                body["password"] is not None:
            token = body["token"]
            redis = await aioredis.create_redis_pool(("api_redis", 6379))
            if await redis.exists(token):
                row = await redis.get(token, encoding='utf-8')
                username, email = row.split(" ")
            else:
                return "need confrim email"

            url = f"http://{self.host}:{self.port}{self.path}/register"
            body.pop("token")
            body['username'] = username
            body['email'] = email
            async with httpx.AsyncClient() as ac:
                r = await ac.post(url, json=body)
            return r.json()
        return "registration fail"

    async def userinfo(self, token):
        url = f"http://{self.host}:{self.port}{self.path}/userinfo"
        headers = {'Authorization': f'Bearer {token.credentials}'}
        async with httpx.AsyncClient() as ac:
            r = await ac.get(url, headers=headers)
        return r.json()

    async def refresh(self, body, token):
        url = f"http://{self.host}:{self.port}{self.path}/refresh"
        headers = {'Authorization': f'Bearer {token.credentials}'}
        async with httpx.AsyncClient() as ac:
            r = await ac.post(url, headers=headers, json=body)
        return r.json()

    async def update(self, body, token):
        url = f"http://{self.host}:{self.port}{self.path}/update"
        headers = {'Authorization': f'Bearer {token.credentials}'}
        async with httpx.AsyncClient() as ac:
            r = await ac.post(url, headers=headers, json=body)
        return r.json()

