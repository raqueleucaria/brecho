# src/repository/sellerRepository.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.model.seller import Seller
from src.model.user import User
from src.schema.sellerSchema import SellerCreate, SellerUpdate


class SellerRepository:
    @staticmethod
    async def get_seller_by_id(
        session: AsyncSession, seller_id: int
    ) -> Seller | None:
        return await session.get(Seller, seller_id)

    @staticmethod
    async def get_seller_by_user_id(
        session: AsyncSession, user_id: int
    ) -> Seller | None:
        return await session.scalar(
            select(Seller).where(Seller.user_id == user_id)
        )

    @staticmethod
    async def get_all_sellers(
        session: AsyncSession, offset: int = 0, limit: int = 100
    ) -> list[Seller]:
        result = await session.scalar(
            select(Seller).offset(offset).limit(limit)
        )
        return list(result.all())

    @staticmethod
    async def create_seller(
        session: AsyncSession, user: User, data: SellerCreate
    ) -> Seller:
        new_seller = Seller(user_id=user.user_id, **data.model_dump())
        session.add(new_seller)
        await session.flush()
        await session.refresh(new_seller)
        return new_seller

    @staticmethod
    async def update_seller(
        session: AsyncSession, db_seller: Seller, data: SellerUpdate
    ) -> Seller:
        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_seller, key, value)

        session.add(db_seller)
        await session.flush()
        await session.refresh(db_seller)
        return db_seller
