import factory
from models import Response
from factory_boy_extra.async_sqlalchemy_factory import AsyncSQLAlchemyModelFactory


class ResponseFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Response

    id = factory.Sequence(lambda n: n)
    message = factory.Faker('paragraph', nb_sentences=5)
