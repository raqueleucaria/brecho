from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.model.checkout import Checkout
from src.model.generate import Generate
from src.model.user import User
from src.repository.cartWantRepository import CartWantRepository
from src.schema.checkoutSchema import CheckoutCreateSchema


class CheckoutService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_checkout_from_cart(
        self, user: User, checkout_data: CheckoutCreateSchema
    ) -> Checkout:
        if not user.client_profile:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail='User is not a client'
            )

        cart_items = await CartWantRepository.get_cart_items_by_client(
            self.session, user.client_profile.client_id
        )
        if not cart_items:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail='Cart is empty'
            )

        if not any(
            addr.address_id == checkout_data.address_id
            for addr in user.addresses
        ):
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail='Invalid address selected',
            )

        try:
            total_products_value = sum(
                item.product.product_price for item in cart_items
            )
            final_total = (
                total_products_value
                + Checkout.SHIPPING_FEE
                - checkout_data.promotion
            )

            new_checkout = Checkout(
                client_id=user.client_profile.client_id,
                promotion=checkout_data.promotion,
                total_value=final_total,
            )
            self.session.add(new_checkout)
            await self.session.flush()

            for item in cart_items:
                self.session.add(
                    Generate(
                        checkout_id=new_checkout.checkout_id,
                        product_id=item.product_id,
                    )
                )

            await CartWantRepository.clear_cart_by_client_id(
                self.session, user.client_profile.client_id
            )

            await self.session.commit()
            await self.session.refresh(new_checkout)

            return new_checkout
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f'An error occurred during checkout: {e}',
            )
