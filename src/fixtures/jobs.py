import factory
from models import Job
from datetime import datetime
from factory_boy_extra.async_sqlalchemy_factory import AsyncSQLAlchemyModelFactory


class JobFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Job

    id = factory.Sequence(lambda n: n)

    title = factory.Faker('job')
    description = factory.Faker('paragraph', nb_sentences=3)

    salary_from = factory.Faker('pyint', min_value=100, max_value=1000000)
    salary_to = factory.Faker('pyint', min_value=100, max_value=1000000)

    is_active = factory.Faker('pybool')
    created_at = factory.LazyFunction(datetime.utcnow)
