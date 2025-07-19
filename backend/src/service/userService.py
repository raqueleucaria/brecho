# src/service/user_service.py
from http import HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException
from src.model.client import Client
from src.model.user import User
from src.repository.userRepository import UserRepository
from src.schema.userSchema import (
    UserSchema,
)


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository()

    async def create_user_with_client_profile(
        self, user_schema: UserSchema, hashed_password: str
    ):
        try:
            new_user = User(
                user_name=user_schema.user_name,
                user_nickname=user_schema.user_nickname,
                user_email=user_schema.user_email,
                user_password=hashed_password,
                user_phone_country_code=user_schema.user_phone_country_code,
                user_phone_state_code=user_schema.user_phone_state_code,
                user_phone_number=user_schema.user_phone_number,
            )

            created_user = await self.user_repo.create_user(self.session, new_user)

            new_client = Client(user_id=created_user.user_id)
            self.session.add(new_client)

            await self.session.commit()
            await self.session.refresh(created_user)

            return created_user
        except Exception:
            await self.session.rollback()
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail='An error occurred while creating the user',
            )
