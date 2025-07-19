from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.model.product import Product


class ProductRepository:
    @staticmethod
    async def create_product(session: AsyncSession, product: Product):
        session.add(product)
        await session.commit()
        await session.refresh(product)
        return product

    @staticmethod
    async def get_products(session: AsyncSession):
        result = await session.scalars(select(Product))
        return result.all()

    @staticmethod
    async def get_product_by_id(session: AsyncSession, product_id: int):
        return await session.scalar(
            select(Product).where(Product.product_id == product_id)
        )

    @staticmethod
    async def delete_product(session: AsyncSession, product: Product):
        try:
            await session.delete(product)
            await session.commit()
            return HTTPStatus.NO_CONTENT
        except Exception as e:
            await session.rollback()
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f'Error deleting product: {str(e)}',
            )

    @staticmethod
    async def update_product(
        session: AsyncSession, product_id: int, update_data: dict
    ):
        product = await ProductRepository.get_product_by_id(
            session, product_id
        )
        if not product:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Product not found',
            )

        for key, value in update_data.items():
            setattr(product, key, value)

        try:
            await session.commit()
            await session.refresh(product)
            return product
        except Exception as e:
            await session.rollback()
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f'Error updating product: {str(e)}',
            )
