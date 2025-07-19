from pydantic import BaseModel, ConfigDict


class ColorSchema(BaseModel):
    color_id: int
    color_name: str
    model_config = ConfigDict(from_attributes=True)


class ColorList(BaseModel):
    colors: list[ColorSchema]
