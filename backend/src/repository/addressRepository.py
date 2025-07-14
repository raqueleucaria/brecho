from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.model.address import Address


class AddressRepository:
    @staticmethod
    async def get_address_by_id(session: AsyncSession, address_id: int):
        result = await session.execute(
            select(Address).where(Address.address_id == address_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_address(session: AsyncSession, user_id: int):
        result = await session.execute(
            select(Address).where(Address.user_id == user_id)
        )
        return result.scalars().all()

    @staticmethod
    async def get_duplicate_address(
        session: AsyncSession, address_data: dict, user_id: int
    ):
        stmt = select(Address).where(
            Address.user_id == user_id,
            Address.address_country == address_data['address_country'],
            Address.address_zip_code == address_data['address_zip_code'],
            Address.address_state == address_data['address_state'],
            Address.address_city == address_data['address_city'],
            Address.address_neighborhood
            == address_data['address_neighborhood'],
            Address.address_street == address_data['address_street'],
            Address.address_number == address_data['address_number'],
            Address.address_complement
            == address_data.get('address_complement'),
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def create_address(
        session: AsyncSession, address_data: dict, user_id: int
    ):
        new_address = Address(**address_data, user_id=user_id)
        session.add(new_address)

        try:
            await session.commit()
            await session.refresh(new_address)
            return new_address
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Address already exists with the same details',
            )

    @staticmethod
    async def update_address(
        session: AsyncSession, address: Address, new_data: dict
    ):
        for key, value in new_data.items():
            setattr(address, key, value)
        try:
            await session.commit()
            await session.refresh(address)
            return address
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Address already exists with the same details',
            )

    @staticmethod
    async def delete_address(session: AsyncSession, address: Address):
        await session.delete(address)
        await session.commit()
