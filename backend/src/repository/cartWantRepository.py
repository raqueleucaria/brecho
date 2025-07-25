from http import HTTPStatus

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.model.cart_want import CartWant, WantType


class CartWantRepository:
    @staticmethod
    async def create_cart_want(session: AsyncSession, cart_want: CartWant):
        session.add(cart_want)
        await session.commit()
        await session.refresh(cart_want)
        return cart_want

    @staticmethod
    async def get_all_id_products(
        session: AsyncSession, client_id: int, want_type: str | None = None
    ):
        query = select(CartWant.product_id).where(
            CartWant.client_id == client_id
        )

        if want_type:
            query = query.filter(CartWant.want_type == want_type)

        result = await session.scalars(query)
        return result.all()

    @staticmethod
    async def get_cart(session: AsyncSession, product_id: int, client_id: int):
        return await session.scalar(
            select(CartWant).where(
                CartWant.product_id == product_id,
                CartWant.client_id == client_id,
            )
        )

    @staticmethod
    async def get_cart_items_by_client(
        session: AsyncSession, client_id: int
    ) -> list[CartWant]:
        query = (
            select(CartWant)
            .where(CartWant.client_id == client_id)
            .where(CartWant.want_type == WantType.cart)
        )
        result = await session.scalars(query)
        return result.all()

    @staticmethod
    async def update_cart_want(
        session: AsyncSession, cart_want: CartWant, update_data: dict
    ):
        for key, value in update_data.items():
            setattr(cart_want, key, value)

        await session.commit()
        await session.refresh(cart_want)
        return cart_want

    @staticmethod
    async def delete_cart_want(session: AsyncSession, cart_want: CartWant):
        await session.delete(cart_want)
        await session.commit()
        return HTTPStatus.NO_CONTENT

    @staticmethod
    async def clear_cart_by_client_id(session: AsyncSession, client_id: int):
        query = (
            delete(CartWant)
            .where(CartWant.client_id == client_id)
            .where(CartWant.want_type == WantType.cart)
        )
        await session.execute(query)
