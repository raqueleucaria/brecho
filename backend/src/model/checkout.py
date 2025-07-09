from sqlalchemy import DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import table_registry

from .client import Client


@table_registry.mapped_as_dataclass
class Checkout:
    __tablename__ = 'tbl_checkout'

    checkout_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    promotion: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    client_id: Mapped[int] = mapped_column(
        ForeignKey(Client.client_id, ondelete='RESTRICT', onupdate='RESTRICT'),
        nullable=False,
    )
