from peewee import PostgresqlDatabase, Model


connection = PostgresqlDatabase(
    'cadastro',
    user='root',
    password='root',
    host='localhost',
    port=5432
)


class BaseModel(Model):
    class Meta:
        database = connection
