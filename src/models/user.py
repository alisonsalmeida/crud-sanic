from src.database import BaseModel
from datetime import datetime

import peewee


class User(BaseModel):
    name = peewee.CharField()
    username = peewee.CharField()
    password = peewee.CharField()
    email = peewee.CharField(unique=True)
    admin = peewee.BooleanField(default=False)

    createdAt = peewee.DateTimeField(default=datetime.utcnow())
    updatedAt = peewee.DateTimeField(default=datetime.utcnow())

    class Meta:
        table_name = '_user'
