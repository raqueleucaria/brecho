from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import table_registry

if TYPE_CHECKING:
    from .address import Address
    from .client import Client
    from .seller import Seller


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'tbl_user'

    user_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_nickname: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True
    )
    user_email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True
    )
    user_name: Mapped[str] = mapped_column(String(255), nullable=False)
    user_password: Mapped[str] = mapped_column(String(255), nullable=False)
    user_phone_country_code: Mapped[str] = mapped_column(
        String(10), nullable=False
    )
    user_phone_state_code: Mapped[str] = mapped_column(
        String(10), nullable=False
    )
    user_phone_number: Mapped[str] = mapped_column(String(20), nullable=False)

    # Relationship
    addresses: Mapped[list['Address']] = relationship(
        init=False,
        cascade='all, delete-orphan',
        lazy='selectin',
    )

    client: Mapped[list['Client']] = relationship(
        init=False,
        back_populates='user',
        lazy='selectin',
    )

    user: Mapped[list['Seller']] = relationship(
        init=False, back_populates='user', lazy='selectin'
    )
