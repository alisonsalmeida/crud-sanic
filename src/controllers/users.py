from sanic.request import Request
from sanic import response
from src.models.user import User
from src.database.database import connection
from peewee_validates import ModelValidator
from playhouse.shortcuts import model_to_dict
from src.utils.serialize import Serialize
from datetime import datetime

import json


class UserController:
    @staticmethod
    async def index(request: Request):
        page = 1
        size = 5
        sizes = [5, 10, 20]

        if 'page' in request.args:
            _page: str = request.args['page'][0]

            if not _page.isnumeric():
                return response.json({'page': 'argument page must be numeric'}, status=400)

            page: int = int(_page)

        if 'size' in request.args:
            _size: str = request.args['size'][0]

            if not _size.isnumeric():
                return response.json({'size': 'argument size must be numeric'}, status=400)

            _size: int = int(_size)
            if _size in sizes:
                size = _size

        users = []
        query = User.select()

        count = query.count()
        pages = (count // size) + 1 if (count % size) > 0 else 0

        query = query.paginate(page=page, paginate_by=size)

        for user in query:
            users.append(user.json)

        data = dict()
        data['pages'] = pages
        data['users'] = users

        return response.json(data, dumps=json.dumps, cls=Serialize)

    @staticmethod
    async def show(request: Request, uid: str):
        user = User.get_or_none(id=uid)

        if user is None:
            return response.json({'user': 'user not found'}, status=404)

        return response.json(user.json, dumps=json.dumps, cls=Serialize)

    @staticmethod
    async def store(request: Request):
        with connection.atomic() as transaction:
            data = request.json

            errors = User.validate(**data)

            if bool(errors):
                return response.json(errors, status=400)

            user: User = User.create(**data)

        return response.json(user, status=201, dumps=json.dumps, cls=Serialize)

    @staticmethod
    async def update(request: Request, uid: str):
        user = User.get_or_none(id=uid)

        if user is None:
            return response.json({'user': 'user not found'}, status=404)

        data = request.json.copy()

        user_dict = user.json
        user_dict.update(data)

        errors = User.validate(**user_dict)

        if bool(errors):
            return response.json(errors, status=400)

        user_dict['updatedAt'] = datetime.utcnow()

        User.update(**user_dict).where(User.id == user.id).execute()

        return response.json(user_dict, dumps=json.dumps, cls=Serialize)

    @staticmethod
    async def destroy(request: Request, uid: str):
        user = User.get_or_none(id=uid)

        if user is None:
            return response.json({'user': 'user not found'}, status=404)

        user.delete_instance(recursive=True)

        return response.empty()
