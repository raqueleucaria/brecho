import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

from src.app import app
from src.database import get_session, table_registry
from src.model.cart_want import WantType
from src.model.checkout import Checkout
from src.model.generate import Generate
from src.security import get_password_hash

from .factories import (
    AddressFactory,
    CartWantFactory,
    CategoryFactory,
    ClientFactory,
    ColorFactory,
    ProductFactory,
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


@pytest_asyncio.fixture
async def user(session):
    user_password = 'testpassword'
    user_obj = UserFactory(user_password=get_password_hash(user_password))

    session.add(user_obj)
    await session.commit()
    await session.refresh(user_obj)

    user_obj.clear_password = user_password

    return user_obj


@pytest_asyncio.fixture
async def other_user(session):
    user_password = 'testpassword'
    user_obj = UserFactory(user_password=get_password_hash(user_password))

    session.add(user_obj)
    await session.commit()
    await session.refresh(user_obj)

    user_obj.clear_password = user_password

    return user_obj


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
    address_obj = AddressFactory(user=user)
    session.add(address_obj)
    await session.commit()

    await session.refresh(user)
    await session.refresh(address_obj)

    return address_obj


@pytest_asyncio.fixture
async def other_address(session, other_user):
    address_obj = AddressFactory(user=other_user)
    session.add(address_obj)
    await session.commit()
    await session.refresh(address_obj)

    return address_obj


@pytest_asyncio.fixture
async def addresses(session, user):
    address_list = AddressFactory.create_batch(3, user=user)
    session.add_all(address_list)
    await session.commit()
    for addr in address_list:
        await session.refresh(addr)

    return address_list


@pytest_asyncio.fixture
async def seller(session, user):
    seller_obj = SellerFactory(user=user)
    session.add(seller_obj)
    await session.commit()
    await session.refresh(seller_obj)

    return seller_obj


@pytest_asyncio.fixture
async def other_seller(session, other_user):
    seller_obj = SellerFactory(user=other_user)
    session.add(seller_obj)
    await session.commit()
    await session.refresh(seller_obj)

    return seller_obj


@pytest_asyncio.fixture
async def category(session):
    category_obj = CategoryFactory()
    session.add(category_obj)
    await session.commit()
    await session.refresh(category_obj)

    return category_obj


@pytest_asyncio.fixture
async def color(session):
    color_obj = ColorFactory()
    session.add(color_obj)
    await session.commit()
    await session.refresh(color_obj)

    return color_obj


@pytest_asyncio.fixture
async def product(session, category, color, seller):
    product_obj = ProductFactory(
        seller_id=seller.seller_id,
        category_id=category.category_id,
        color_id=color.color_id,
    )
    session.add(product_obj)
    await session.commit()
    await session.refresh(product_obj)

    return product_obj


@pytest_asyncio.fixture
async def other_product(session, other_seller, category, color):
    product_obj = ProductFactory(
        seller_id=other_seller.seller_id,
        category_id=category.category_id,
        color_id=color.color_id,
    )
    session.add(product_obj)
    await session.commit()
    await session.refresh(product_obj)

    return product_obj


@pytest_asyncio.fixture
async def client_profile(session, user):
    client_obj = ClientFactory(user=user)
    session.add(client_obj)
    await session.commit()
    await session.refresh(client_obj)

    return client_obj


@pytest_asyncio.fixture
async def cart_want(session, product, client_profile):
    cart_want_obj = CartWantFactory(
        product_id=product.product_id,
        client_id=client_profile.client_id,
        want_type=WantType.cart,
    )
    session.add(cart_want_obj)
    await session.commit()
    await session.refresh(cart_want_obj)

    return cart_want_obj


@pytest_asyncio.fixture
async def checkout(session, client_profile, product):
    checkout_obj = Checkout(client_id=client_profile.client_id, promotion=0.0)
    session.add(checkout_obj)
    await session.commit()
    await session.refresh(checkout_obj)

    generate_entry = Generate(
        checkout_id=checkout_obj.checkout_id, product_id=product.product_id
    )
    session.add(generate_entry)
    await session.commit()
    await session.refresh(checkout_obj)

    return checkout_obj
