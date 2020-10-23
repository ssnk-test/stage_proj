from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.security.http import HTTPBearer
from typing import Optional
from fastapi import Depends
from datetime import datetime

from api_app.services.users import UserServiceAPI
from api_app.services.email import EmailServiceAPI
from api_app.services.goods import GoodsServiceAPI
from api_app.services.monitoring import MonServiceAPI


class LoginBody(BaseModel):
    username: str
    password: str


class UpdateBody(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None


class RegisterBody(UpdateBody):
    token: Optional[str] = None


class AddTemplatesBody(BaseModel):
    name: str
    body: str


class RefreshBody(BaseModel):
    rtoken: str


class AddItemBody(BaseModel):
    head: Optional[str] = None
    body: Optional[str] = None
    price: Optional[int] = None
    tag: Optional[int] = None
    image: Optional[str] = None

class EventModel(BaseModel):
    service: str
    url: str
    status: str
    req_time: str
    res_time: str



bearer_scheme = HTTPBearer()
router = APIRouter()


# users service
@router.post("/user/login")
async def login(item: LoginBody):
    a = UserServiceAPI()
    return await a.login(dict(item))


@router.post("/user/register")
async def register(item: RegisterBody):
    a = UserServiceAPI()
    return await a.register(dict(item))


@router.post("/user/logout")
async def logout(token: str = Depends(bearer_scheme)):
    a = UserServiceAPI()
    return await a.logout(token)


@router.get("/user/userinfo")
async def view_userinfo(token: str = Depends(bearer_scheme)):
    a = UserServiceAPI()
    return await a.userinfo(token)


@router.post("/user/refresh")
async def refresh(item: RefreshBody, token: str = Depends(bearer_scheme)):
    a = UserServiceAPI()
    return await a.refresh(dict(item), token)


@router.post("/user/update")
async def login(item: UpdateBody, token: str = Depends(bearer_scheme)):
    a = UserServiceAPI()
    return await a.update(dict(item), token)


# email service
@router.get("/email/templates")
async def view_templates():
    a = EmailServiceAPI()
    return await a.view()


@router.post("/email/template")
async def add_template(item: AddTemplatesBody):
    a = EmailServiceAPI()
    return await a.add(dict(item))


# goods service
@router.get("/goods/tags")
async def view_tags():
    a = GoodsServiceAPI()
    return await a.view_tags()


@router.get("/goods/items")
async def view_items():
    a = GoodsServiceAPI()
    return await a.view_items()

@router.post("/goods/items")
async def add_items(item: AddItemBody, token: str = Depends(bearer_scheme)):
    a = GoodsServiceAPI()
    return await a.add_items(dict(item), token)

@router.post("/goods/items/{pk}")
async def view_item(pk):
    a = GoodsServiceAPI()
    return await a.view_item(pk)

@router.patch("/goods/items/{pk}")
async def modify_item(pk, item: AddItemBody, token: str = Depends(bearer_scheme)):
    a = GoodsServiceAPI()
    return await a.modify_items(pk, dict(item), token)

@router.delete("/goods/items/{pk}")
async def delete_item(pk, token: str = Depends(bearer_scheme)):
    a = GoodsServiceAPI()
    return await a.delete_item(pk, token)

# Monitoring service
@router.get("/mon/events")
async def view_events():
    a = MonServiceAPI()
    return await a.view_events()

@router.post("/mon/events")
async def add_event(item: EventModel):
    a = MonServiceAPI()
    return await a.add_event(dict(item))


