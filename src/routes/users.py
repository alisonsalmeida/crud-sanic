from sanic import Blueprint
from sanic.request import Request
from src.controllers.users import UserController


user = Blueprint('content_user', url_prefix='/users')


@user.get('/')
async def index(request: Request):
    return await UserController.index(request)


@user.get('/<uid>')
async def show(request: Request, uid):
    return await UserController.show(request, uid)


@user.post('/')
async def store(request: Request):
    return await UserController.store(request)


@user.delete('/<uid>')
async def destroy(request: Request, uid):
    return await UserController.destroy(request, uid)


@user.put('/<uid>')
async def update(request: Request, uid):
    return await UserController.update(request, uid)
