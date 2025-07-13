from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.model.user import User
from src.repository.addressRepository import AddressRepository
from src.schema.addressSchema import AddressPublic, AddressSchema
from src.security import get_current_user

router = APIRouter(prefix='/address', tags=['address'])

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get('/', response_model=list[AddressPublic])
async def get_addresses(user: CurrentUser, session: Session):
    return await AddressRepository.get_address(session, user.user_id)


@router.post('/', response_model=AddressPublic, status_code=HTTPStatus.CREATED)
async def create_address(
    address: AddressSchema,
    user: CurrentUser,
    session: Session,
):
    address_data = address.model_dump()
    return await AddressRepository.create_address(
        session, address_data, user.user_id
    )


@router.put('/{address_id}', response_model=AddressPublic)
async def update_address(
    address_id: int,
    address: AddressSchema,
    current_user: CurrentUser,
    session: Session,
):
    if current_user.user_id != address.user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions',
        )

    db_address = await AddressRepository.get_address_by_id(session, address_id)

    if not db_address:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Address not found'
        )

    if db_address.user_id != current_user.user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You do not have permission to change this address.',
        )

    address_data = address.address_schema.model_dump()

    return await AddressRepository.update_address(
        session, db_address, address_data
    )


@router.delete('/{address_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_address(
    address_id: int,
    current_user: CurrentUser,
    session: Session,
):
    db_address = await AddressRepository.get_address_by_id(session, address_id)

    if not db_address:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Address not found'
        )

    if db_address.user_id != current_user.user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You do not have permission to delete this address.',
        )

    await AddressRepository.delete_address(session, db_address)
    return HTTPStatus.NO_CONTENT
