from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import table_registry

if TYPE_CHECKING:  # pragma: no cover
    from .user import User
    from .cart_want import CartWant


@table_registry.mapped_as_dataclass
class Client:
    __tablename__ = 'tbl_client'

    client_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            'tbl_user.user_id', ondelete='RESTRICT', onupdate='RESTRICT'
        ),
        nullable=False,
    )

    user: Mapped['User'] = relationship(
        back_populates='client_profile', init=False
    )

    cart_wants: Mapped[list['CartWant']] = relationship(
        back_populates='client',
        init=False,
        lazy='selectin',
        cascade='all, delete-orphan',
    )