from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.model.user import User
from src.repository.sellerRepository import SellerRepository
from src.schema.messageSchema import Message
from src.schema.sellerSchema import (
    SellerCreate,
    SellerList,
    SellerPrivate,
    SellerPublic,
    SellerUpdate,
)
from src.security import get_current_user

router = APIRouter(prefix='/seller', tags=['seller'])
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get('/{seller_id}', response_model=SellerPublic)
async def get_seller_by_id(session: Session, seller_id: int):
    seller = await SellerRepository.get_seller_by_id(session, seller_id)

    if not seller:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return SellerPublic.model_validate(seller)


@router.get('/', response_model=SellerList, status_code=HTTPStatus.OK)
async def list_sellers(session: Session):
    sellers = await SellerRepository.get_sellers(session)
    return {'sellers': sellers}


@router.get('/me', response_model=SellerPrivate)
async def get_my_seller_profile(user: CurrentUser, session: Session):
    seller_profile = await SellerRepository.get_seller_by_user_id(
        session, user.user_id
    )
    if not seller_profile:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return SellerPrivate.model_validate(seller_profile)


@router.post('/', status_code=HTTPStatus.CREATED, response_model=SellerPrivate)
async def create_seller_profile(
    seller: SellerCreate, user: CurrentUser, session: Session
):
    return await SellerRepository.create_seller(
        session, user.user_id, seller.dict()
    )


@router.patch('/me{seller_id}', response_model=SellerPrivate)
async def patch_seller(
    seller_id: int,
    seller_data: SellerUpdate,
    user: CurrentUser,
    session: Session,
):
    db_seller = await SellerRepository.get_seller_by_id(
        session, user.user_id, seller_id
    )
    if not db_seller:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    updated_seller = seller_data.model_dump(exclude_unset=True)
    return await SellerRepository.update_seller(
        session, db_seller, updated_seller
    )


@router.delete('/me{seller_id}', response_model=Message)
async def delete_seller(
    seller_id: int,
    user: CurrentUser,
    session: Session,
):
    db_seller = await SellerRepository.get_seller_by_id(
        session, user.user_id, seller_id
    )
    if not db_seller:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return await SellerRepository.delete_seller(session, db_seller)
