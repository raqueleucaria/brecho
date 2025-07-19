from sqlalchemy.ext.asyncio import AsyncSession

from src.model.checkout import Checkout


class CheckoutRepository:
    @staticmethod
    async def get_checkout_by_id(
        session: AsyncSession, checkout_id: int
    ) -> Checkout | None:
        return await session.get(Checkout, checkout_id)
