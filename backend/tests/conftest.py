from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from src.app import app
from src.database import get_session
from src.models import User, table_registry
from src.security import get_password_hash


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


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


@pytest.fixture
def user(session):
    user_password = 'testtest'
    user = User(
        user_name='Teste',
        user_nickname='Teste Nick',
        user_email='teste@test.com',
        user_password=get_password_hash(user_password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

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
def another_user(session):
    user = User(
        user_name='Other',
        user_nickname='OtherNick',
        user_email='other@example.com',
        user_password=get_password_hash('otherpass'),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    user.user_clear_password = 'otherpass'
    return user
