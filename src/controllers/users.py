from sanic.request import Request
from sanic import response
from src.models.user import User
from src.database.database import connection
from peewee_validates import ModelValidator
from playhouse.shortcuts import model_to_dict
from src.utils.serialize import Serialize

import json


class UserController:
    @staticmethod
    async def index(request: Request):
        users = []
        query = User.select()

        for user in query:
            _user = model_to_dict(user, recurse=False, backrefs=True)
            users.append(_user)

        return response.json(users, dumps=json.dumps, cls=Serialize)

    @staticmethod
    async def show(request: Request, uid: str):
        user = User.get_or_none(id=uid)

        if user is None:
            return response.json({'user': 'user not found'}, status=404)

        _user = model_to_dict(user, recurse=False, backrefs=True)
        return response.json(_user, dumps=json.dumps, cls=Serialize)

    @staticmethod
    async def store(request: Request):
        with connection.atomic() as transaction:
            data = request.json
            print(data, request.json)

            validator = ModelValidator(User(**data))
            validator.validate()

            if bool(validator.errors):
                return response.json(validator.errors, status=400)

            user: User = User.create(**data)
            _user = model_to_dict(user, recurse=False, backrefs=True)

        # _user = json.dumps(_user, cls=Serialize)
        #              dumps(body, **kwargs)

        return response.json(_user, status=201, dumps=json.dumps, cls=Serialize)

    @staticmethod
    async def destroy(request: Request, uid: str):
        pass

    @staticmethod
    async def update(request: Request, uid: str):
        pass
