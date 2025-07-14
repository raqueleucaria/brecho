from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.model.color import Color


class ColorRepository:
    @staticmethod
    async def get_all_colors(
        session: AsyncSession, offset: int = 0, limit: int = 10
    ):
        result = await session.scalars(
            select(Color).offset(offset).limit(limit)
        )
        return result.all()

    @staticmethod
    async def get_by_id(session: AsyncSession, color_id: int):
        result = await session.execute(
            select(Color).where(Color.color_id == color_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_name(session: AsyncSession, color_name: str):
        result = await session.execute(
            select(Color).where(Color.color_name == color_name)
        )
        return result.scalar_one_or_none()
