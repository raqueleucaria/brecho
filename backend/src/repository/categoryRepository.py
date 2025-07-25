from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.model.category import Category


class CategoryRepository:
    @staticmethod
    async def get_categories(session: AsyncSession):
        result = await session.scalars(select(Category))
        return result.all()

    @staticmethod
    async def get_category_by_id(session: AsyncSession, category_id: int):
        result = await session.execute(
            select(Category).where(Category.category_id == category_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_name(session: AsyncSession, category_name: str):
        result = await session.execute(
            select(Category).where(Category.category_name == category_name)
        )
        return result.scalar_one_or_none()
