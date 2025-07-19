from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from src.model.product import (
    ProductCondition,
    ProductGender,
    ProductSize,
    ProductStatus,
)


class ProductSchema(BaseModel):
    product_name: str = Field(..., max_length=100)
    product_price: float = Field(..., ge=0)
    product_description: str | None = Field(..., max_length=500)
    product_condition: ProductCondition = Field(
        ..., description='Condition of the product: available or unavailable'
    )
    product_gender: ProductGender = Field(
        ..., description='Gender of the product: F, M, or U'
    )
    product_size: ProductSize = Field(..., description='Size of the product')
    category_id: int | None = Field(
        None, description='ID of the category to which the product belongs'
    )
    color_id: int | None = Field(
        None, description='ID of the color of the product'
    )
    product_status: ProductStatus = Field(
        default=ProductStatus.available,
        description='Status of the product: available or unavailable',
    )
    model_config = ConfigDict(from_attributes=True)


class ProductPublic(ProductSchema):
    product_id: int
    seller_id: int
    model_config = ConfigDict(from_attributes=True)


class ProductList(BaseModel):
    products: list[ProductPublic]


class ProductUpdate(BaseModel):
    product_name: Optional[str] = Field(default=None, max_length=100)
    product_price: Optional[float] = Field(default=None, ge=0)
    product_description: Optional[str] = Field(default=None, max_length=500)
    product_condition: Optional[ProductCondition] = Field(
        default=None,
        description='Condition of the product: available or unavailable',
    )
    product_gender: Optional[ProductGender] = Field(
        default=None, description='Gender of the product: F, M, or U'
    )
    product_size: Optional[ProductSize] = Field(
        default=None, description='Size of the product'
    )
    category_id: Optional[int] = Field(
        default=None,
        description='ID of the category to which the product belongs',
    )
    color_id: Optional[int] = Field(
        default=None, description='ID of the color of the product'
    )
    product_status: Optional[ProductStatus] = Field(
        default=None,
        description='Status of the product: available or unavailable',
    )
    model_config = ConfigDict(from_attributes=True)
