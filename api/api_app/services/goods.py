import httpx
from api_app.services.users import UserServiceAPI
from jose import jwt
import jose

class GoodsServiceAPI:
    def __init__(self):
        self.host = "goods_service"
        self.port = "8000"
        self.path = ""

    async def view_tags(self):
        url = f"http://{self.host}:{self.port}{self.path}/tags/"
        async with httpx.AsyncClient() as ac:
            r = await ac.get(url)

        return r.json()

    async def view_items(self):
        url = f"http://{self.host}:{self.port}{self.path}/items"
        async with httpx.AsyncClient() as ac:
            r = await ac.get(url)
        return r.json()

    async def add_items(self, body, token):
        # проверим валидность токена обращением к сервису user
        a = UserServiceAPI()
        resp = await a.userinfo(token)
        b = dict(resp)
        if b['response'] != 'ok':
            return {"response": "invalid auth token"}

        # token ok
        body.pop('image')
        body['user_uuid'] = b["uuid"]

        url = f"http://{self.host}:{self.port}{self.path}/items/"

        async with httpx.AsyncClient() as ac:
            r = await ac.post(url, json=body)

        return r.json()

    async def view_item(self, pk):
        url = f"http://{self.host}:{self.port}{self.path}/items/{str(pk)}/"
        async with httpx.AsyncClient() as ac:
            r = await ac.get(url)
        return r.json()

    async def modify_item(self, pk, body, token):
        # проверим валидность токена обращением к сервису user
        a = UserServiceAPI()
        resp = await a.userinfo(token)
        test_access = dict(resp)

        # получим юзера из токена
        try:
            access_token_jwt = jwt.decode(
                token.credentials,
                'yfibgjtplfcfvstgjtplfnst'
            )
        except jose.exceptions.JWTError:
            return {"response": "invalid auth token"}

        if test_access['response'] != 'ok':
            return {"response": "invalid auth token"}

        # может ли юзер редактировать объявление

        write_acess = await self.view_item(pk)

        if write_acess['user_uuid'] != access_token_jwt['uuid']:
            return {"response": "no acess"}

        # token ok & write access ok
        body.pop('image')
        body['user_uuid'] = test_access["uuid"]

        url = f"http://{self.host}:{self.port}{self.path}/items/{str(pk)}/"

        async with httpx.AsyncClient() as ac:
            r = await ac.patch(url, json=body)
        return r.json()

    async def delete_item(self, pk,  token):
        # проверим валидность токена обращением к сервису user
        a = UserServiceAPI()
        resp = await a.userinfo(token)
        test_access = dict(resp)

        # получим юзера из токена
        try:
            access_token_jwt = jwt.decode(
                token.credentials,
                'yfibgjtplfcfvstgjtplfnst'
            )
        except jose.exceptions.JWTError:
            return {"response": "invalid auth token"}

        if test_access['response'] != 'ok':
            return {"response": "invalid auth token"}

        # может ли юзер редактировать объявление

        write_acess = await self.view_item(pk)

        if write_acess['user_uuid'] != access_token_jwt['uuid']:
            return {"response": "no acess"}

        # token ok & write access ok

        url = f"http://{self.host}:{self.port}{self.path}/items/{str(pk)}/"

        async with httpx.AsyncClient() as ac:
            r = await ac.delete(url)
            if r.status_code == 204:
                return {"response": "deleted"}
        return {"response": "not deleted"}
