from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import table_registry

from .order_payment import OrderPayment


@table_registry.mapped_as_dataclass
class Pix:
    __tablename__ = 'tbl_pix'

    pix_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    pix_key: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True
    )
    pix_expiry_date: Mapped[str] = mapped_column(DateTime, nullable=False)
    order_id: Mapped[int] = mapped_column(
        ForeignKey(
            OrderPayment.order_id,
            ondelete='RESTRICT',
            onupdate='RESTRICT',
        ),
        nullable=False,
    )
