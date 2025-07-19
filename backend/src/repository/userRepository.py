from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.model.user import User


class UserRepository:
    @staticmethod
    async def get_users(
        session: AsyncSession, offset: int = 0, limit: int = 10
    ):
        result = await session.scalars(
            select(User).offset(offset).limit(limit)
        )
        return result.all()

    @staticmethod
    async def get_user_by_nickname_or_email(
        session: AsyncSession, nickname: str, email: str
    ):
        return await session.scalar(
            select(User).where(
                (User.user_nickname == nickname) | (User.user_email == email)
            )
        )

    @staticmethod
    async def create_user(session: AsyncSession, user: User):
        session.add(user)
        await session.flush()
        await session.refresh(user)
        return user

    @staticmethod
    async def update_user(
        session: AsyncSession, db_user: User, user_data: dict
    ):
        for key, value in user_data.items():
            setattr(db_user, key, value)
        try:
            await session.commit()
            await session.refresh(db_user)
            return db_user
        except IntegrityError:
            await session.rollback()
            raise

    @staticmethod
    async def delete_user(session: AsyncSession, db_user: User):
        await session.delete(db_user)
        await session.commit()
