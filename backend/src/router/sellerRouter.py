from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.model.user import User
from src.repository.sellerRepository import SellerRepository
from src.schema.filterSchema import FilterPage
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


@router.get('/', response_model=SellerList, status_code=HTTPStatus.OK)
async def list_sellers(
    session: Session,
    pagination: Annotated[FilterPage, Depends()],
):
    sellers_from_db = await SellerRepository.get_all_sellers(
        session, offset=pagination.offset, limit=pagination.limit
    )
    return {'sellers': sellers_from_db}


@router.get('/{seller_id}', response_model=SellerPublic)
async def get_seller_profile(seller_id: int, session: Session):
    db_seller = await SellerRepository.get_seller_by_id(session, seller_id)

    if not db_seller:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Seller profile not found.',
        )

    return db_seller


@router.get('/me', response_model=SellerPrivate)
async def get_my_seller_profile(current_user: CurrentUser, session: Session):
    db_seller = await SellerRepository.get_seller_by_user_id(
        session, current_user.user_id
    )
    if not db_seller:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Seller profile not found.',
        )
    return db_seller


@router.post('/', status_code=HTTPStatus.CREATED, response_model=SellerPrivate)
async def create_seller_profile(
    data: SellerCreate, current_user: CurrentUser, session: Session
):
    if await SellerRepository.get_seller_by_user_id(
        session, current_user.user_id
    ):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Seller profile already exists for this user.',
        )

    db_seller = await SellerRepository.create_seller(
        session, current_user, data
    )
    await session.commit()
    return db_seller


@router.put('/me', response_model=SellerPrivate)
async def update_my_seller_profile(
    data: SellerUpdate, current_user: CurrentUser, session: Session
):
    db_seller = await SellerRepository.get_seller_by_user_id(
        session, current_user.user_id
    )
    if not db_seller:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Seller profile not found.',
        )

    updated_seller = await SellerRepository.update_seller(
        session, db_seller, data
    )
    await session.commit()
    return updated_seller
