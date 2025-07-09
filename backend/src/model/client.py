from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import table_registry

from .user import User


@table_registry.mapped_as_dataclass
class Client:
    __tablename__ = 'tbl_client'

    client_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(User.user_id, ondelete='RESTRICT', onupdate='RESTRICT'),
        nullable=False,
    )
