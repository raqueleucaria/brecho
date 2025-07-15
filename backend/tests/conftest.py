from contextlib import contextmanager
from datetime import datetime

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

from src.app import app
from src.database import get_session, table_registry
from src.security import get_password_hash

from .factories import (
    AddressFactory,
    CategoryFactory,
    ColorFactory,
    SellerFactory,
    UserFactory,
)


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
    # def fake_time_hook(mapper, connection, target):
    #     if hasattr(target, 'user_created_at'):
    #         target.user_created_at = time
    #     if hasattr(target, 'user_updated_at'):
    #         target.user_updated_at = time

    # event.listen(model, 'before_insert', fake_time_hook)
    yield time
    # event.remove(model, 'before_insert', fake_time_hook)


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


@pytest.fixture
def other_token(client, other_user):
    response = client.post(
        '/auth/token',
        data={
            'username': other_user.user_email,
            'password': other_user.clear_password,
        },
    )
    return response.json()['access_token']


@pytest_asyncio.fixture
async def address(session, user):
    address = AddressFactory(user=user)
    session.add(address)
    await session.commit()
    await session.refresh(address)

    address.clear_password = user.clear_password

    return address


@pytest_asyncio.fixture
async def other_address(session, other_user):
    address = AddressFactory(user_id=other_user.user_id)
    session.add(address)
    await session.commit()
    await session.refresh(address)

    address.clear_password = other_user.clear_password

    return address


@pytest_asyncio.fixture
async def addresses(session, user):
    address = AddressFactory(user_id=user.user_id)
    session.add_all(addresses)
    await session.commit()
    for address in addresses:
        await session.refresh(address)

    return addresses


@pytest_asyncio.fixture
async def seller(session, user):
    seller = SellerFactory(user_id=user.user_id)
    session.add(seller)
    await session.commit()
    await session.refresh(seller)

    return seller


@pytest_asyncio.fixture
async def category(session):
    category = CategoryFactory()
    session.add(category)
    await session.commit()
    await session.refresh(category)

    return category


@pytest_asyncio.fixture
async def color(session):
    color = [ColorFactory() for _ in range(3)]
    session.add_all(color)
    await session.commit()
    for color in color:
        await session.refresh(color)

    return color
