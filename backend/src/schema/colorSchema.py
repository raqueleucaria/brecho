from pydantic import BaseModel


class ColorSchema(BaseModel):
    color_id: int
    color_name: str


class ColorList(BaseModel):
    colors: list[ColorSchema]


class ColorPublic(BaseModel):
    color_name: str

    class Config:
        from_attributes = True
