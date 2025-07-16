from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.model.seller import Seller


class SellerRepository:
    @staticmethod
    async def get_seller_by_id(session: AsyncSession, seller_id: int):
        return await session.scalar(
            select(Seller).where(Seller.seller_id == seller_id)
        )

    @staticmethod
    async def get_seller_by_user_id(session: AsyncSession, user_id: int):
        return await session.scalar(
            select(Seller).where(Seller.user_id == user_id)
        )

    @staticmethod
    async def create_seller(session: AsyncSession, seller: Seller):
        session.add(seller)
        await session.commit()
        await session.refresh(seller)
        return seller

    @staticmethod
    async def get_sellers(session: AsyncSession):
        result = await session.scalars(select(Seller))
        return result.all()

    @staticmethod
    async def get_user_id_by_seller_id(session: AsyncSession, seller_id: int):
        return await session.scalar(
            select(Seller.user_id).where(Seller.seller_id == seller_id)
        )

    @staticmethod
    async def update_seller(
        session: AsyncSession, db_seller: Seller, update_data: dict
    ):
        for key, value in update_data.items():
            setattr(db_seller, key, value)
        try:
            await session.commit()
            await session.refresh(db_seller)
            return db_seller
        except IntegrityError:
            await session.rollback()
            raise
