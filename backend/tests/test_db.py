from dataclasses import asdict

import pytest
from sqlalchemy import create_engine, select, text

from src.model.user import User
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
async def test_create_user(session):
    new_user = User(
        user_name='test',
        user_nickname='test_nick',
        user_password='secret',
        user_email='teste@test',
        user_phone_country_code='+55',
        user_phone_state_code='11',
        user_phone_number='123456789',
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
        'user_phone_country_code': '+55',
        'user_phone_state_code': '11',
        'user_phone_number': '123456789',
    }
