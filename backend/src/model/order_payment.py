import enum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import table_registry

if TYPE_CHECKING:
    from .boleto import Boleto
    from .card import Card
    from .checkout import Checkout
    from .pix import Pix


class OrderStatus(enum.Enum):
    pending = 'pending'
    paid = 'paid'
    shipped = 'shipped'
    delivered = 'delivered'
    cancelled = 'cancelled'
    expired = 'expired'


class PaymentMethod(enum.Enum):
    credit_card = 'credit_card'
    debit_card = 'debit_card'
    boleto = 'boleto'
    pix = 'pix'


class Tracking(enum.Enum):
    shipped = 'shipped'
    in_transit = 'in_transit'
    delivered = 'delivered'
    returned = 'returned'


@table_registry.mapped_as_dataclass
class OrderPayment:
    __tablename__ = 'tbl_order_payment'

    order_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    order_number: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True
    )
    order_date: Mapped[str] = mapped_column(DateTime, nullable=False)
    order_updated_at: Mapped[str] = mapped_column(DateTime, nullable=True)
    payment_method: Mapped[PaymentMethod] = mapped_column(
        Enum(PaymentMethod), nullable=False
    )
    payment_date: Mapped[str] = mapped_column(DateTime, nullable=True)
    order_tracking: Mapped[Tracking] = mapped_column(
        Enum(Tracking), nullable=True
    )
    checkout_id: Mapped[int] = mapped_column(
        ForeignKey(
            'tbl_checkout.checkout_id',
            ondelete='RESTRICT',
            onupdate='RESTRICT',
        ),
        nullable=False,
    )
    order_status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus),
        nullable=False,
        default=OrderStatus.pending,
        server_default='pending',
    )

    # --- RELACIONAMENTOS ---
    checkout: Mapped['Checkout'] = relationship(init=False)

    pix_details: Mapped['Pix'] = relationship(
        init=False, cascade='all, delete-orphan'
    )
    boleto_details: Mapped['Boleto'] = relationship(
        init=False, cascade='all, delete-orphan'
    )
    card_details: Mapped['Card'] = relationship(
        init=False, cascade='all, delete-orphan'
    )
