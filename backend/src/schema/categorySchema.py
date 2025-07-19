from pydantic import BaseModel, ConfigDict


class CategorySchema(BaseModel):
    category_id: int
    category_name: str
    model_config = ConfigDict(from_attributes=True)


class CategoryList(BaseModel):
    categories: list[CategorySchema]
