from sanic import Blueprint
from .users import user


routes = Blueprint.group([user], url_prefix='/app')
