from datetime import date, datetime
from typing import Union

from pydantic import BaseModel, ConfigDict

from src.model.order_payment import OrderStatus, PaymentMethod, Tracking


# --- Schemas de Detalhes de Pagamento (para a resposta) ---
class PixPublic(BaseModel):
    pix_key: str
    pix_expiry_date: datetime
    model_config = ConfigDict(from_attributes=True)


class BoletoPublic(BaseModel):
    boleto_bar_code: str
    boleto_expiry_date: date
    model_config = ConfigDict(from_attributes=True)


class CardPublic(BaseModel):
    card_number: str  # Apenas os últimos 4 dígitos em um app real
    model_config = ConfigDict(from_attributes=True)


# --- Schemas de Criação (o que o cliente envia) ---
class CardDetailsCreate(BaseModel):
    card_number: str
    card_expiry_date: str  # Ex: "12/28"
    card_holder_name: str
    card_holder_national_code: str  # CPF


class OrderCreateSchema(BaseModel):
    checkout_id: int
    payment_method: PaymentMethod
    card_details: CardDetailsCreate | None = None


# --- Schemas de Atualização (o que um admin ou sistema usaria) ---
class OrderStatusUpdateSchema(BaseModel):
    order_status: OrderStatus


class OrderTrackingUpdateSchema(BaseModel):
    order_tracking: Tracking


# --- Schema de Resposta Principal ---
class OrderPublicSchema(BaseModel):
    order_id: int
    order_number: str
    order_date: datetime
    order_status: OrderStatus
    payment_method: PaymentMethod
    total_value: float

    payment_details: Union[PixPublic, BoletoPublic, CardPublic, None] = None

    model_config = ConfigDict(from_attributes=True)
