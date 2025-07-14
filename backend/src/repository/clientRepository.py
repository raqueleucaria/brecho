from sqlalchemy.ext.asyncio import AsyncSession

from src.model.client import Client
from src.model.user import User


class ClientRepository:
    @staticmethod
    async def create_client_for_user(session: AsyncSession, user: User):
        new_client = Client(user_id=user.user_id)
        session.add(new_client)

        return new_client
