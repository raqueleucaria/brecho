from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import table_registry


@table_registry.mapped_as_dataclass
class Category:
    __tablename__ = 'tbl_category'

    category_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    category_name: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True
    )
