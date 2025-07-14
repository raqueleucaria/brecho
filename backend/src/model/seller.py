import enum
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import table_registry

if TYPE_CHECKING:  # pragma: no cover
    from .user import User


class SellerStatus(enum.Enum):
    active = 'active'
    inactive = 'inactive'


class BankType(enum.Enum):
    checking = 'checking'
    savings = 'savings'


@table_registry.mapped_as_dataclass
class Seller:
    __tablename__ = 'tbl_seller'

    seller_id: Mapped[int] = mapped_column(init=False, primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            'tbl_user.user_id', ondelete='RESTRICT', onupdate='RESTRICT'
        ),
        nullable=False,
    )

    seller_description: Mapped[str] = mapped_column(String(500), nullable=True)

    seller_bank_account: Mapped[str] = mapped_column(String(7), nullable=False)
    seller_bank_agency: Mapped[str] = mapped_column(String(6), nullable=False)
    seller_bank_name: Mapped[str] = mapped_column(String(100), nullable=False)
    seller_bank_type: Mapped[BankType] = mapped_column(
        Enum(BankType, name='bank_type', create_type=False), nullable=False
    )

    seller_status: Mapped[SellerStatus] = mapped_column(
        Enum(SellerStatus, name='seller_status', create_type=False),
        nullable=False,
        default=SellerStatus.inactive,
        server_default='inactive',
    )

    user: Mapped['User'] = relationship(
        back_populates='seller_profile',
        init=False,
    )
