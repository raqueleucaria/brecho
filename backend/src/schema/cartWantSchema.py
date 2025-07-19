from pydantic import BaseModel, ConfigDict, Field

from src.model.cart_want import WantType


class CartWantSchema(BaseModel):
    product_id: int = Field(..., description='ID of the product in the cart')
    client_id: int = Field(
        ..., description='ID of the client who wants the product'
    )
    want_type: WantType = Field(
        ..., description='Type of want: cart or wishlist'
    )

    model_config = ConfigDict(from_attributes=True)


class CartWantProduct(BaseModel):
    product_id: int = Field(..., description='ID of the product in the cart')
    model_config = ConfigDict(from_attributes=True)


class CartWantList(CartWantProduct):
    cart_wants: list[CartWantSchema]


class CartWantUpdate(BaseModel):
    want_type: WantType | None = Field(
        default=None, description='Type of want: cart or wishlist'
    )

    model_config = ConfigDict(from_attributes=True)


class CartWantCreateSchema(BaseModel):
    product_id: int = Field(..., description='ID of the product to add')
    want_type: WantType = Field(
        ..., description='Type of want: cart or wishlist'
    )


class CartWantFilter(BaseModel):
    want_type: WantType | None = Field(
        default=None, description='Filter by want type: cart or wishlist'
    )
