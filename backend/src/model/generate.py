from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import table_registry

from .checkout import Checkout
from .product import Product


@table_registry.mapped_as_dataclass
class Generate:
    __tablename__ = 'tbl_generate'

    checkout_id: Mapped[int] = mapped_column(
        ForeignKey(
            Checkout.checkout_id, ondelete='RESTRICT', onupdate='RESTRICT'
        ),
        primary_key=True,
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey(
            Product.product_id, ondelete='RESTRICT', onupdate='RESTRICT'
        ),
        primary_key=True,
    )
