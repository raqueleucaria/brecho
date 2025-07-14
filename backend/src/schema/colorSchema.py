from pydantic import BaseModel


class ColorSchema(BaseModel):
    color_id: int
    color_name: str


class ColorList(BaseModel):
    colors: list[ColorSchema]
