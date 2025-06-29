# from datetime import datetime

# from sqlalchemy import func, String
# from sqlalchemy.orm import Mapped, mapped_column, registry

# table_registry = registry()


# @table_registry.mapped_as_dataclass
# class User:
#     __tablename__ = 'users'

#     user_id: Mapped[int] = mapped_column(init=False, primary_key=True)
#     user_name: Mapped[str] = mapped_column(String(255), nullable=False)
#     user_nickname: Mapped[str] = mapped_column(String(255),  nullable=False, unique=True)
#     user_email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
#     user_password: Mapped[str] = mapped_column(String(255), nullable=False)
#     user_created_at: Mapped[datetime] = mapped_column(
#         init=False, server_default=func.now()
#     )
#     user_updated_at: Mapped[datetime] = mapped_column(
#         init=False, server_default=func.now(), onupdate=func.now()
#     )
