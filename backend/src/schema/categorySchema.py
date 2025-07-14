from pydantic import BaseModel


class CategorySchema(BaseModel):
    category_id: int
    category_name: str


class CategoryList(BaseModel):
    categories: list[CategorySchema]
