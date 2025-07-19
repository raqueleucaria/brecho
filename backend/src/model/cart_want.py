from typing import TYPE_CHECKING

import enum

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import table_registry

if TYPE_CHECKING:  # pragma: no cover
    from .client import Client
    from .product import Product


class WantType(enum.Enum):
    cart = 'cart'
    wishlist = 'wishlist'


@table_registry.mapped_as_dataclass
class CartWant:
    __tablename__ = 'tbl_cart_want'

    product_id: Mapped[int] = mapped_column(
        ForeignKey(
            'tbl_product.product_id', ondelete='RESTRICT', onupdate='RESTRICT'
        ),
        primary_key=True,
    )
    client_id: Mapped[int] = mapped_column(
        ForeignKey('tbl_client.client_id', ondelete='RESTRICT', onupdate='RESTRICT'),
        primary_key=True,
    )
    want_type: Mapped[WantType] = mapped_column(Enum(WantType), nullable=False)

    product: Mapped['Product'] = relationship(
        init=False,
        back_populates='cart_wants',
        uselist=False,
        lazy='joined',
    )

    client: Mapped['Client'] = relationship(
        init=False,
        back_populates='cart_wants',
        uselist=False,
        lazy='joined',
    )