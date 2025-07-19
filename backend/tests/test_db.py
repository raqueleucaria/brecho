from dataclasses import asdict

import pytest
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import noload

from src.model.address import Address
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
        'addresses': [],
        'client_profile': None,
        'seller_profile': None,
    }


@pytest.mark.asyncio
async def test_create_address(session, user):
    address_data = Address(
        address_country='Brasil',
        address_zip_code='12345-678',
        address_state='SP',
        address_city='São Paulo',
        address_neighborhood='Centro',
        address_street='Rua Exemplo',
        address_number='123',
        address_complement='Apto 456',
        user_id=user.user_id,
    )
    session.add(address_data)
    await session.commit()

    query = select(Address).options(noload(Address.user))
    fetched_address = await session.scalar(query)

    address_dict = asdict(fetched_address)
    address_dict.pop('user', None)

    assert address_dict == {
        'address_id': 1,
        'address_country': 'Brasil',
        'address_zip_code': '12345-678',
        'address_state': 'SP',
        'address_city': 'São Paulo',
        'address_neighborhood': 'Centro',
        'address_street': 'Rua Exemplo',
        'address_number': '123',
        'address_complement': 'Apto 456',
        'user_id': 1,
    }


@pytest.mark.asyncio
async def test_user_address_relationship(session, user: User):
    address = Address(
        address_country='Brasil',
        address_zip_code='12345-678',
        address_state='SP',
        address_city='São Paulo',
        address_neighborhood='Centro',
        address_street='Rua Exemplo',
        address_number='123',
        address_complement='Apto 456',
        user_id=user.user_id,
    )

    session.add(address)
    await session.commit()
    await session.refresh(user)

    user = await session.scalar(
        select(User).where(User.user_id == user.user_id)
    )

    assert user.addresses == [address]


# @pytest.mark.asyncio
# async def test_get_session_executes_and_yields_session():
#     session_generator = get_session()

#     async for session in session_generator:
#         assert isinstance(session, AsyncSession)
#         assert session.is_active

#         result = await session.execute(text('SELECT 1'))
#         assert result.scalar_one() == 1
