import uuid
from datetime import datetime, timedelta
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.model.boleto import Boleto
from src.model.card import Card
from src.model.order_payment import (
    OrderPayment,
    OrderStatus,
    PaymentMethod,
    Tracking,
)
from src.model.pix import Pix
from src.model.user import User
from src.repository.checkoutRepository import CheckoutRepository
from src.schema.orderPaymentSchema import (
    OrderCreateSchema,
    OrderStatusUpdateSchema,
    OrderTrackingUpdateSchema,
)


class OrderService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_order_from_checkout(
        self, user: User, order_data: OrderCreateSchema
    ) -> OrderPayment:
        checkout = await CheckoutRepository.get_checkout_by_id(
            self.session, order_data.checkout_id
        )

        if not checkout or checkout.client_id != user.client_profile.client_id:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Checkout not found'
            )

        try:
            new_order = OrderPayment(
                order_number=str(uuid.uuid4()),
                order_date=datetime.now(),
                payment_method=order_data.payment_method,
                checkout_id=checkout.checkout_id,
            )
            self.session.add(new_order)
            await self.session.flush()

            if order_data.payment_method == PaymentMethod.pix:
                new_order.pix_details = Pix(
                    pix_key=str(uuid.uuid4()),
                    pix_expiry_date=datetime.now() + timedelta(hours=1),
                )

            elif order_data.payment_method == PaymentMethod.boleto:
                new_order.boleto_details = Boleto(
                    boleto_bar_code=''.join(str(i) for i in range(48)),
                    boleto_expiry_date=datetime.now().date()
                    + timedelta(days=3),
                )

            elif order_data.payment_method == PaymentMethod.credit_card:
                if not order_data.card_details:
                    raise HTTPException(
                        status_code=HTTPStatus.BAD_REQUEST,
                        detail='Card details required',
                    )
                new_order.card_details = Card(
                    **order_data.card_details.model_dump()
                )

            await self.session.commit()
            await self.session.refresh(new_order)
            return new_order

        except Exception as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f'An error occurred while creating the order: {e}',
            )

    async def update_order_status(
        self, order_id: int, status_update: OrderStatusUpdateSchema
    ) -> OrderPayment:
        """
        Simula a atualização do status de um pedido (ex: webhook de pagamento).
        """
        order = await self.order_repo.get_order_by_id(self.session, order_id)
        if not order:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Order not found'
            )

        order.order_status = status_update.order_status
        order.order_updated_at = datetime.now()

        # SIMULAÇÃO: Se o status for 'paid', registra a data do pagamento.
        if status_update.order_status == OrderStatus.paid:
            order.payment_date = datetime.now()

        return await self.order_repo.save(self.session, order)

    async def update_tracking_status(
        self, order_id: int, tracking_update: OrderTrackingUpdateSchema
    ) -> OrderPayment:
        """
        Simula a atualização do rastreamento de um pedido.
        """
        order = await self.order_repo.get_order_by_id(self.session, order_id)
        if not order:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Order not found'
            )

        order.order_tracking = tracking_update.order_tracking
        order.order_updated_at = datetime.now()

        # SIMULAÇÃO: Se o rastreio for 'shipped', atualiza o status do pedido.
        if tracking_update.order_tracking == Tracking.shipped:
            order.order_status = OrderStatus.shipped

        return await self.order_repo.save(self.session, order)
