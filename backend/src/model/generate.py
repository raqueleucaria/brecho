from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import table_registry

if TYPE_CHECKING:  # pragma: no cover
    from .checkout import Checkout
    from .product import Product


@table_registry.mapped_as_dataclass
class Generate:
    __tablename__ = 'tbl_generate'

    checkout_id: Mapped[int] = mapped_column(
        ForeignKey(
            'tbl_checkout.checkout_id',
            ondelete='RESTRICT',
            onupdate='RESTRICT',
        ),
        primary_key=True,
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey(
            'tbl_product.product_id', ondelete='RESTRICT', onupdate='RESTRICT'
        ),
        primary_key=True,
    )

    product: Mapped['Product'] = relationship(
        init=False,
        back_populates='generate_entries',
        uselist=False,
        lazy='joined',
    )

    checkout: Mapped['Checkout'] = relationship(
        init=False,
        back_populates='products_generated',
        uselist=False,
        lazy='joined',
    )
