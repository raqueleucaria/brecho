from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import table_registry

if TYPE_CHECKING:
    from .order_payment import OrderPayment


@table_registry.mapped_as_dataclass
class Boleto:
    __tablename__ = 'tbl_boleto'

    boleto_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    boleto_bar_code: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True
    )
    boleto_expiry_date: Mapped[str] = mapped_column(Date, nullable=False)
    order_id: Mapped[int] = mapped_column(
        ForeignKey(
            'tbl_order_payment.order_id',
            ondelete='RESTRICT',
            onupdate='RESTRICT',
        ),
        nullable=False,
    )
    order: Mapped['OrderPayment'] = relationship(
        init=False, back_populates='boleto_details'
    )
