from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.model.seller import Seller
from src.model.user import User
from src.repository.sellerRepository import SellerRepository
from src.schema.sellerSchema import (
    SellerList,
    SellerPrivate,
    SellerPublic,
    SellerSchema,
)
from src.security import get_current_user

router = APIRouter(prefix='/seller', tags=['seller'])
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=SellerPublic, status_code=HTTPStatus.CREATED)
async def create_seller(
    seller: SellerSchema, session: Session, user: CurrentUser
):
    db_seller = await SellerRepository.get_seller_by_user_id(
        session, user.user_id
    )

    if db_seller:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Seller profile already exists for this user',
        )

    seller = Seller(
        seller_description=seller.seller_description,
        seller_bank_account=seller.seller_bank_account,
        seller_bank_agency=seller.seller_bank_agency,
        seller_bank_name=seller.seller_bank_name,
        seller_bank_type=seller.seller_bank_type,
        seller_status=seller.seller_status,
        user_id=user.user_id,
    )

    return await SellerRepository.create_seller(session, seller)


@router.get('/', response_model=SellerList)
async def read_sellers(session: Session):
    sellers = await SellerRepository.get_sellers(session)

    return {'sellers': sellers}


@router.put(
    '/{seller_id}', response_model=SellerPrivate, status_code=HTTPStatus.OK
)
async def update_seller(
    seller_id: int,
    seller: SellerSchema,
    session: Session,
    user: CurrentUser,
):
    db_seller = await SellerRepository.get_seller_by_id(session, seller_id)
    if not db_seller:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Seller not found'
        )

    db_user_id = await SellerRepository.get_user_id_by_seller_id(
        session, seller_id
    )

    if user.user_id != db_user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You do not have permission to update this seller profile',
        )

    seller_data = {
        'seller_description': seller.seller_description,
        'seller_bank_account': seller.seller_bank_account,
        'seller_bank_agency': seller.seller_bank_agency,
        'seller_bank_name': seller.seller_bank_name,
        'seller_bank_type': seller.seller_bank_type,
        'seller_status': seller.seller_status,
    }

    return await SellerRepository.update_seller(
        session, db_seller, seller_data
    )
