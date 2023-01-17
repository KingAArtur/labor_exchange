import asyncio
from asyncio import get_event_loop

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fixtures.users import UserFactory
from fixtures.jobs import JobFactory
from fixtures.responses import ResponseFactory
from fastapi.testclient import TestClient
from main import app
import pytest
import pytest_asyncio
from unittest.mock import MagicMock
from db_settings import SQLALCHEMY_DATABASE_URL
from dependencies import get_db, get_current_user


@pytest_asyncio.fixture()
async def sa_session():
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL) # You must provide your database URL.
    connection = await engine.connect()
    trans = await connection.begin()

    Session = sessionmaker(connection, expire_on_commit=False, class_=AsyncSession)
    session = Session()

    async def mock_delete(instance):
        session.expunge(instance)
        return await asyncio.sleep(0)

    session.commit = MagicMock(side_effect=session.flush)
    session.delete = MagicMock(side_effect=mock_delete)

    try:
        yield session
    finally:
        await session.close()
        await trans.rollback()
        await connection.close()
        await engine.dispose()


@pytest_asyncio.fixture()
async def current_user(sa_session: AsyncSession):
    new_user = UserFactory.build()
    sa_session.add(new_user)
    await sa_session.commit()
    await sa_session.refresh(new_user)
    return new_user


# регистрация фабрик
@pytest_asyncio.fixture(autouse=True)
def setup_factories(sa_session: AsyncSession) -> None:
    UserFactory.session = sa_session
    JobFactory.session = sa_session
    ResponseFactory.session = sa_session


@pytest_asyncio.fixture()
def client_app(sa_session):
    app.dependency_overrides[get_db] = lambda: sa_session
    client = TestClient(app, backend_options={"use_uvloop": True})
    with client as c:
        yield c