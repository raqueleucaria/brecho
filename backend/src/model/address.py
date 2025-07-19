from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import table_registry

if TYPE_CHECKING:  # pragma: no cover
    from .user import User


@table_registry.mapped_as_dataclass
class Address:
    __tablename__ = 'tbl_address'

    address_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    address_country: Mapped[str] = mapped_column(String(100), nullable=False)
    address_zip_code: Mapped[str] = mapped_column(String(20), nullable=False)
    address_state: Mapped[str] = mapped_column(String(100), nullable=False)
    address_city: Mapped[str] = mapped_column(String(100), nullable=False)
    address_neighborhood: Mapped[str] = mapped_column(
        String(100), nullable=False
    )
    address_street: Mapped[str] = mapped_column(String(255), nullable=False)
    address_number: Mapped[str] = mapped_column(String(5), nullable=False)
    address_complement: Mapped[str] = mapped_column(String(255), nullable=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            'tbl_user.user_id', ondelete='RESTRICT', onupdate='RESTRICT'
        ),
        nullable=False,
    )

    user: Mapped['User'] = relationship(
        init=False, back_populates='addresses', uselist=False
    )
