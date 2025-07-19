from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:  # pragma: no cover
    from .product import Product

from src.database import table_registry


@table_registry.mapped_as_dataclass
class Color:
    __tablename__ = 'tbl_color'

    color_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    color_name: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True
    )

    products: Mapped[list['Product']] = relationship(
        back_populates='color',
        init=False,
        cascade='all, delete-orphan',
        lazy='selectin',
    )
