from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.model.address import Address
from src.model.user import User
from src.schema.addressSchema import AddressPublic, AddressSchema
from src.repository.addressRepository import AddressRepository
from src.security import get_current_user

router = APIRouter()

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix='/address', tags=['address'])


@router.get('/', response_model=list[AddressPublic])
async def get_addresses(user: CurrentUser, session: Session):
    addresses = await UserRepository.get_address(
        session, user.user_id
    )
    return {'addresses': addresses}


@router.post('/', response_model=AddressPublic)
async def create_address(
    address: AddressSchema,
    user: CurrentUser,
    session: Session,
):
    address_data = address.dict()
    duplicate = await AddressRepository.get_duplicate_address(
        session, address_data, user.user_id
    )
    if duplicate:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Endereço já cadastrado com os mesmos dados',
        )

    new_address = Address(**address_data, user_id=user.user_id)
    return await AddressRepository.create_address(session, new_address)
   

@router.put('/{address_id}', response_model=AddressPublic)
async def update_address(
    address_id: int,
    address: AddressSchema,
    current_user: CurrentUser,
    session: Session,
):
    if current_user.user_id != address.user_id:
        raise HTTPStatus(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions',
        )
    
    db_address = await AddressRepository.get_address_by_id(session, address_id)

    if not db_address:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Endereço não encontrado"
        )

    address_data = address.dict()
    duplicate = await AddressRepository.get_duplicate_address(
        session, address_data, current_user.user_id
    )
    if duplicate and duplicate.address_id != db_address.address_id:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Outro endereço com os mesmos dados já existe',
        )