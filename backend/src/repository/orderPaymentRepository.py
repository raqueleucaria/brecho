from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.model.order_payment import OrderPayment


class OrderRepository:
    @staticmethod
    async def get_order_by_id(
        session: AsyncSession, order_id: int
    ) -> OrderPayment | None:
        return await session.get(OrderPayment, order_id)

    @staticmethod
    async def get_orders_by_client_id(
        session: AsyncSession, client_id: int
    ) -> list[OrderPayment]:
        query = select(OrderPayment).where(
            OrderPayment.checkout.has(client_id=client_id)
        )
        result = await session.scalars(query)
        return result.all()

    @staticmethod
    async def save(session: AsyncSession, order: OrderPayment) -> OrderPayment:
        await session.commit()
        await session.refresh(order)
        return order
