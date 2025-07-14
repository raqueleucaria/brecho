from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.model.user import User
from src.repository.addressRepository import AddressRepository
from src.schema.addressSchema import (
    AddressPublic,
    AddressSchema,
    AddressUpdate,
)
from src.schema.messageSchema import Message
from src.security import get_current_user

router = APIRouter(prefix='/address', tags=['address'])

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get('/', response_model=list[AddressPublic])
async def get_addresses(
    session: Session,
    user: CurrentUser,
):
    return await AddressRepository.get_address(session, user.user_id)


@router.post('/', response_model=AddressPublic, status_code=HTTPStatus.CREATED)
async def create_address(
    address: AddressSchema,
    user: CurrentUser,
    session: Session,
):
    return await AddressRepository.create_address(
        session, address.dict(), user.user_id
    )


@router.patch('/{address_id}', response_model=AddressPublic)
async def patch_address(
    address_id: int,
    address_data: AddressUpdate,
    session: Session,
    user: CurrentUser,
):
    db_address = await AddressRepository.get_address_by_id(
        session, user.user_id, address_id
    )

    if not db_address:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Address not found'
        )

    if db_address.user_id != user.user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You do not have permission to change this address.',
        )

    update_data = address_data.model_dump(exclude_unset=True)
    return await AddressRepository.update_address(
        session, db_address, update_data
    )


@router.delete('/{address_id}', response_model=Message)
async def delete_address(
    address_id: int,
    user: CurrentUser,
    session: Session,
):
    db_address = await AddressRepository.get_address_by_id(
        session, user.user_id, address_id
    )

    if not db_address:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Address not found'
        )

    if db_address.user_id != user.user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You do not have permission to delete this address.',
        )

    return await AddressRepository.delete_address(session, db_address)
