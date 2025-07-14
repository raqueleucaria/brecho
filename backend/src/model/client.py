from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import table_registry

if TYPE_CHECKING:
    from .user import User


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
