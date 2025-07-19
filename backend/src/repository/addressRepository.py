from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.model.address import Address


class AddressRepository:
    @staticmethod
    async def get_address_by_id(
        session: AsyncSession, user_id: int, address_id: int
    ):
        result = await session.execute(
            select(Address).where(
                Address.user_id == user_id, Address.address_id == address_id
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_addresses_by_user_id(session: AsyncSession, user_id: int):
        result = await session.scalars(
            select(Address).where(Address.user_id == user_id)
        )
        return result.all()

    @staticmethod
    async def create_address(session: AsyncSession, address: Address):
        session.add(address)
        await session.commit()
        await session.refresh(address)
        return address

    @staticmethod
    async def update_address(
        session: AsyncSession, db_address: Address, update_data: dict
    ):
        for key, value in update_data.items():
            setattr(db_address, key, value)

        session.add(db_address)
        await session.commit()
        await session.refresh(db_address)
        return db_address

    @staticmethod
    async def delete_address(session: AsyncSession, address: Address):
        await session.delete(address)
        await session.commit()
        return {'message': 'Address deleted successfully'}
