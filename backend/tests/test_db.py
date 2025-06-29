from dataclasses import asdict

import pytest
from sqlalchemy import create_engine, select, text

from src.models import User
from src.settings import Settings

settings = Settings()
engine = create_engine(settings.DATABASE_URL)

try:
    with engine.connect() as conn:
        result = conn.execute(text('SELECT 1'))
        print('Conexão bem-sucedida!', result.scalar())
except Exception as e:
    print('Erro ao conectar:', e)


@pytest.mark.asyncio
async def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            user_name='test',
            user_nickname='test_nick',
            user_password='secret',
            user_email='teste@test',
        )
        session.add(new_user)
        await session.commit()
    user = await session.scalar(select(User).where(User.user_name == 'test'))
    # breakpoint()
    assert asdict(user) == {
        'user_id': 1,
        'user_name': 'test',
        'user_nickname': 'test_nick',
        'user_password': 'secret',
        'user_email': 'teste@test',
        'user_created_at': time,
        'user_updated_at': time,
    }
