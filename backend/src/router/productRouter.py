from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.model.product import Product
from src.model.user import User
from src.repository.productRepository import ProductRepository
from src.schema.productSchema import (
    ProductList,
    ProductPublic,
    ProductSchema,
    ProductUpdate,
)
from src.security import (
    get_current_user,
)

router = APIRouter(prefix='/product', tags=['product'])
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=ProductPublic, status_code=HTTPStatus.CREATED)
async def create_product(
    product: ProductSchema, session: Session, user: CurrentUser
):
    product = Product(
        product_name=product.product_name,
        product_price=product.product_price,
        product_description=product.product_description,
        product_condition=product.product_condition,
        product_gender=product.product_gender,
        product_size=product.product_size,
        category_id=product.category_id,
        color_id=product.color_id,
        seller_id=user.seller_profile.seller_id,
        product_status=product.product_status,
    )

    return await ProductRepository.create_product(session, product)


@router.get('/', response_model=ProductList)
async def read_products(session: Session):
    products = await ProductRepository.get_products(session)
    return {'products': products}


@router.get('/{product_id}', response_model=ProductPublic)
async def read_product(product_id: int, session: Session):
    product = await ProductRepository.get_product_by_id(session, product_id)
    if not product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Product not found',
        )
    return product


@router.delete('/{product_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_product(product_id: int, session: Session, user: CurrentUser):
    product = await ProductRepository.get_product_by_id(session, product_id)
    if not product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Product not found',
        )

    if product.seller_id != user.seller_profile.seller_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You do not have permission to delete this product',
        )

    return await ProductRepository.delete_product(session, product)


@router.patch('/{product_id}', response_model=ProductPublic)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    session: Session,
    user: CurrentUser,
):
    product = await ProductRepository.get_product_by_id(session, product_id)
    if not product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Product not found',
        )

    if product.seller_id != user.seller_profile.seller_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You do not have permission to update this product',
        )

    update_product = product_update.model_dump(exclude_unset=True)

    if not update_product:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='No update data provided',
        )

    return await ProductRepository.update_product(
        session, product.product_id, update_product
    )
