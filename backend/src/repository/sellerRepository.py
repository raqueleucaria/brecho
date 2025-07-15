from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.model.seller import Seller


class SellerRepository:
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

    # @staticmethod
    # async def get_seller_by_id(session: AsyncSession, seller_id: int):
    #     return await session.scalar(
    #         select(Seller).where(Seller.seller_id == seller_id)
    #     )

    # @staticmethod
    # async def get_sellers(session: AsyncSession):
    #     result = await session.scalars(select(Seller))
    #     return result.all()

    # @staticmethod
    # async def create_seller(session: AsyncSession, user_id: int, seller: dict):
    #     new_seller = Seller(user_id=user_id, **seller)
    #     session.add(new_seller)
    #     await session.flush()
    #     await session.refresh(new_seller)
    #     return new_seller

    # @staticmethod
    # async def update_seller(
    #     session: AsyncSession, db_seller: Seller, update_data: dict
    # ):
    #     for key, value in update_data.items():
    #         setattr(db_seller, key, value)

    #     session.add(db_seller)
    #     await session.flush()
    #     await session.refresh(db_seller)
    #     return db_seller
