from pydantic import BaseModel, ConfigDict


class CheckoutCreateSchema(BaseModel):
    address_id: int
    promotion: float = 0.0


class CheckoutPublicSchema(BaseModel):
    checkout_id: int
    client_id: int
    promotion: float
    total_value: float
    product_ids: list[int]

    model_config = ConfigDict(from_attributes=True)
