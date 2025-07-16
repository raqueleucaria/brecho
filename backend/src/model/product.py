import enum
from typing import TYPE_CHECKING

from sqlalchemy import DECIMAL, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import table_registry

# from .category import Category
# from .color import Color
# from .seller import Seller

if TYPE_CHECKING:  # pragma: no cover
    from .category import Category
    from .color import Color
    from .seller import Seller


class ProductStatus(enum.Enum):
    available = 'available'
    unavailable = 'unavailable'


class ProductCondition(enum.Enum):
    new = 'new'
    used = 'used'


class ProductGender(enum.Enum):
    female = 'F'
    male = 'M'
    unisex = 'U'


class ProductSize(enum.Enum):
    XS = 'XS'
    S = 'S'
    M = 'M'
    L = 'L'
    XL = 'XL'
    XXL = 'XXL'
    XXXL = 'XXXL'
    _34 = '34'
    _36 = '36'
    _38 = '38'
    _40 = '40'
    _42 = '42'
    _44 = '44'
    _46 = '46'
    _48 = '48'
    other = 'other'


@table_registry.mapped_as_dataclass
class Product:
    __tablename__ = 'tbl_product'

    product_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    product_name: Mapped[str] = mapped_column(String(100), nullable=False)
    product_price: Mapped[float] = mapped_column(
        DECIMAL(10, 2), nullable=False
    )
    product_description: Mapped[str] = mapped_column(
        String(500), nullable=True
    )
    product_condition: Mapped[ProductCondition] = mapped_column(
        Enum(ProductCondition), nullable=False
    )
    product_gender: Mapped[ProductGender] = mapped_column(
        Enum(ProductGender), nullable=False
    )
    product_size: Mapped[str] = mapped_column(
        Enum(ProductSize, name='product_size', create_type=False),
        nullable=False,
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey(
            'tbl_category.category_id',
            ondelete='RESTRICT',
            onupdate='RESTRICT',
        ),
        nullable=False,
    )
    color_id: Mapped[int] = mapped_column(
        ForeignKey(
            'tbl_color.color_id', ondelete='RESTRICT', onupdate='RESTRICT'
        ),
        nullable=False,
    )
    seller_id: Mapped[int] = mapped_column(
        ForeignKey(
            'tbl_seller.seller_id', ondelete='RESTRICT', onupdate='RESTRICT'
        ),
        nullable=False,
    )

    product_status: Mapped[ProductStatus] = mapped_column(
        Enum(ProductStatus),
        nullable=False,
        default=ProductStatus.available,
        server_default='available',
    )

    seller: Mapped['Seller'] = relationship(
        back_populates='products',
        init=False,
    )

    category: Mapped['Category'] = relationship(
        init=False,
        back_populates='products',
        lazy='selectin',
        uselist=False,
    )

    color: Mapped['Color'] = relationship(
        init=False,
        back_populates='products',
        lazy='selectin',
        uselist=False,
    )
