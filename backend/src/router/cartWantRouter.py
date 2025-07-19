from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.model.cart_want import CartWant
from src.model.user import User
from src.repository.cartWantRepository import CartWantRepository
from src.repository.productRepository import ProductRepository
from src.schema.cartWantSchema import (
    CartWantCreateSchema,
    # CartWantListSchema,
    CartWantFilter,
    CartWantSchema,
    CartWantUpdate,
)
from src.security import (
    get_current_user,
)

router = APIRouter(prefix='/cart-want', tags=['cart-want'])
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    '/', response_model=CartWantSchema, status_code=HTTPStatus.CREATED
)
async def create_cart_want(
    cart_want: CartWantCreateSchema,
    session: Session,
    user: CurrentUser,
):
    product = await ProductRepository.get_product_by_id(
        session, cart_want.product_id
    )

    if not product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Product not found'
        )

    new_cart_want = CartWant(
        product_id=cart_want.product_id,
        client_id=user.client_profile.client_id,
        want_type=cart_want.want_type,
    )

    return await CartWantRepository.create_cart_want(session, new_cart_want)


@router.get(
    '/',
    response_model=list[int],
    description="IDs of products in the client's where want type is 'cart'",
)
async def list_cart_by_client_id(
    session: Session,
    user: CurrentUser,
    cart_want_filter: Annotated[CartWantFilter, Depends()],
):
    product_ids = await CartWantRepository.get_cart_want_by_client_id(
        session, user.client_profile.client_id, cart_want_filter.want_type
    )
    return product_ids


@router.patch(
    '/',
    response_model=CartWantSchema,
    status_code=HTTPStatus.OK,
)
async def update_cart_want(
    product_id: int,
    client_id: int,
    update_data: CartWantUpdate,
    session: Session,
    user: CurrentUser,
):
    cart_want = await CartWantRepository.get_cart_want_by_ids(
        session, product_id, client_id
    )

    if not cart_want:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Cart want not found'
        )

    if cart_want.client_id != user.client_profile.client_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You do not have permission to update this cart want',
        )

    update_cart_want = update_data.model_dump(exclude_unset=True)

    if not update_cart_want:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='No data provided for update',
        )

    return await CartWantRepository.update_cart_want(
        session, cart_want, update_cart_want
    )


@router.delete(
    '/',
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete_cart_want(
    product_id: int,
    client_id: int,
    session: Session,
    user: CurrentUser,
):
    cart_want = await CartWantRepository.get_cart_want_by_ids(
        session, product_id, client_id
    )

    if not cart_want:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Cart want not found'
        )

    if cart_want.client_id != user.client_profile.client_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You do not have permission to delete this cart want',
        )

    return await CartWantRepository.delete_cart_want(session, cart_want)
