from contextlib import contextmanager
from datetime import datetime

import factory
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

from src.app import app
from src.database import get_session
from src.model.user import User, table_registry
from src.security import get_password_hash


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


# alternando fixture de sessão para usar AsyncSession
@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(
        'sqlite+aiosqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@contextmanager
def _mock_db_time(*, model, time=datetime(2025, 1, 1)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'user_created_at'):
            target.user_created_at = time
        if hasattr(target, 'user_updated_at'):
            target.user_updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)
    yield time
    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest_asyncio.fixture
async def user(session):
    user_password = 'testtest'
    user = UserFactory(user_password=get_password_hash(user_password))

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clear_password = user_password

    return user


@pytest_asyncio.fixture
async def other_user(session):
    user_password = 'testtest'
    user = UserFactory(user_password=get_password_hash(user_password))

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clear_password = user_password

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': user.user_email,
            'password': user.clear_password,
        },
    )
    return response.json()['access_token']


class UserFactory(factory.Factory):
    class Meta:
        model = User

    user_name = factory.Sequence(lambda n: f'test{n}')
    user_nickname = factory.LazyAttribute(lambda obj: f'{obj.user_name}_nick')
    user_email = factory.LazyAttribute(
        lambda obj: f'{obj.user_name}@email.com'
    )
    user_password = factory.LazyAttribute(
        lambda obj: f'{obj.user_name}_password'
    )
