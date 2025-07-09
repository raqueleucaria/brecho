from datetime import datetime

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'tbl_user'

    user_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_name: Mapped[str] = mapped_column(String(255), nullable=False)
    user_nickname: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True
    )
    user_email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True
    )
    user_password: Mapped[str] = mapped_column(String(255), nullable=False)
    user_phone_country_code: Mapped[str] = mapped_column(
        String(10), nullable=False
    )
    user_phone_state_code: Mapped[str] = mapped_column(
        String(10), nullable=False
    )
    user_phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
