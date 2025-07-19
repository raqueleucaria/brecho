from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.model.user import User
from src.repository.orderPaymentRepository import OrderRepository
from src.schema.orderPaymentSchema import (
    OrderCreateSchema,
    OrderPublicSchema,
    OrderStatusUpdateSchema,
    OrderTrackingUpdateSchema,
)
from src.security import get_current_user
from src.service.orderPaymentService import OrderService

router = APIRouter(prefix='/orders', tags=['orders'])
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=OrderPublicSchema
)
async def create_order(
    order_data: OrderCreateSchema,
    session: Session,
    user: CurrentUser,
):
    order_service = OrderService(session)
    return await order_service.create_order_from_checkout(user, order_data)


@router.get('/', response_model=list[OrderPublicSchema])
async def list_client_orders(session: Session, user: CurrentUser):
    """Lista todas as ordens do cliente autenticado."""
    return await OrderRepository.get_orders_by_client_id(
        session, user.client_profile.client_id
    )


@router.get('/{order_id}', response_model=OrderPublicSchema)
async def get_order_details(
    order_id: int, session: Session, user: CurrentUser
):
    """Busca os detalhes de uma ordem específica."""
    order = await OrderRepository.get_order_by_id(session, order_id)

    if not order or order.checkout.client_id != user.client_profile.client_id:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Order not found'
        )
    return order


@router.patch('/{order_id}/status', response_model=OrderPublicSchema)
async def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdateSchema,
    session: Session,
):
    order_service = OrderService(session)
    return await order_service.update_order_status(order_id, status_update)


@router.patch('/{order_id}/tracking', response_model=OrderPublicSchema)
async def update_tracking_status(
    order_id: int,
    tracking_update: OrderTrackingUpdateSchema,
    session: Session,
):
    order_service = OrderService(session)
    return await order_service.update_tracking_status(
        order_id, tracking_update
    )
