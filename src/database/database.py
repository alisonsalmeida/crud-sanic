from peewee import PostgresqlDatabase, Model
from peewee_validates import ModelValidator
from playhouse.shortcuts import model_to_dict


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

    @property
    def json(self):
        return None

    @json.getter
    def json(self) -> dict:
        return model_to_dict(self, backrefs=True, recurse=False)

    @json.setter
    def json(self, value):
        pass

    @classmethod
    def validate(cls, **data) -> dict:
        validator = ModelValidator(cls(**data))
        validator.validate()

        return validator.errors
