from sqlalchemy import DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import table_registry

from .address import Address
from .checkout import Checkout


@table_registry.mapped_as_dataclass
class Analyse:
    __tablename__ = 'tbl_analyse'

    checkout_id: Mapped[int] = mapped_column(
        ForeignKey(
            Checkout.checkout_id, ondelete='RESTRICT', onupdate='RESTRICT'
        ),
        primary_key=True,
    )
    address_id: Mapped[int] = mapped_column(
        ForeignKey(
            Address.address_id, ondelete='RESTRICT', onupdate='RESTRICT'
        ),
        primary_key=True,
    )
    shipping_fee: Mapped[float] = mapped_column(DECIMAL(6, 2), nullable=False)
