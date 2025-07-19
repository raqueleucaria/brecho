from typing import TYPE_CHECKING

from sqlalchemy import DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import table_registry

if TYPE_CHECKING:
    from .generate import Generate


@table_registry.mapped_as_dataclass
class Checkout:
    __tablename__ = 'tbl_checkout'

    promotion: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    client_id: Mapped[int] = mapped_column(
        ForeignKey(
            'tbl_client.client_id', ondelete='RESTRICT', onupdate='RESTRICT'
        ),
        nullable=False,
    )

    checkout_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    products_generated: Mapped[list['Generate']] = relationship(
        init=False, lazy='selectin', back_populates='checkout'
    )

    SHIPPING_FEE: float = 15.00

    @property
    def total_value(self) -> float:
        total_products = sum(
            generate.product.product_price
            for generate in self.products_generated
        )
        return (total_products + self.SHIPPING_FEE) - self.promotion

    @property
    def product_ids(self) -> list[int]:
        return [generate.product_id for generate in self.products_generated]
