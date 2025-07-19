from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.model.user import User
from src.repository.checkoutRepository import CheckoutRepository
from src.schema.checkoutSchema import (
    CheckoutCreateSchema,
    CheckoutPublicSchema,
)
from src.security import get_current_user
from src.service.checkoutService import CheckoutService

router = APIRouter(prefix='/checkout', tags=['checkout'])
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=CheckoutPublicSchema
)
async def create_checkout(
    checkout_data: CheckoutCreateSchema,
    session: Session,
    user: CurrentUser,
):
    checkout_service = CheckoutService(session)
    return await checkout_service.create_checkout_from_cart(
        user, checkout_data
    )


@router.get('/{checkout_id}', response_model=CheckoutPublicSchema)
async def get_checkout_details(
    checkout_id: int, session: Session, user: CurrentUser
):
    checkout = await CheckoutRepository.get_checkout_by_id(
        session, checkout_id
    )

    if not checkout or checkout.client_id != user.client_profile.client_id:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Checkout not found'
        )

    return checkout
