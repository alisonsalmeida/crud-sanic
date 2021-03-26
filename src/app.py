from sanic import Sanic
from .routes import routes
from src.database.database import connection
from src.models.user import User


app = Sanic(__name__)
app.blueprint(routes)


@app.listener('before_server_start')
async def create_tables(server: Sanic, _):
    try:
        connection.create_tables(
            [User]
        )

    except Exception as e:
        pass


@app.listener('after_server_start')
async def depois(server: Sanic, _):
    pass
