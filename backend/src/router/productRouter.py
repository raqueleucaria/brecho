from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.model.product import Product
from src.model.user import User
from src.repository.productRepository import ProductRepository
from src.schema.productSchema import ProductPublic, ProductSchema
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
