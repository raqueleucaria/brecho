from sqlalchemy.ext.asyncio import AsyncSession

from src.model.product import Product


class ProductRepository:
    @staticmethod
    async def create_product(session: AsyncSession, product: Product):
        session.add(product)
        await session.commit()
        await session.refresh(product)
        return product
