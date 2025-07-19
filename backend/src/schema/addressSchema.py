from pydantic import BaseModel, ConfigDict, Field


class AddressSchema(BaseModel):
    address_country: str
    address_zip_code: str
    address_state: str
    address_city: str
    address_neighborhood: str
    address_street: str
    address_number: str = Field(..., max_length=5)
    address_complement: str | None = None

    model_config = ConfigDict(from_attributes=True)


class AddressPublic(AddressSchema):
    address_id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class AddressList(AddressPublic):
    addresses: list[AddressPublic]


class AddressUpdate(AddressSchema):
    address_country: str | None = None
    address_zip_code: str | None = None
    address_state: str | None = None
    address_city: str | None = None
    address_neighborhood: str | None = None
    address_street: str | None = None
    address_number: str | None = Field(..., max_length=5)
    address_complement: str | None = None


class AddressPublicSchema(BaseModel):
    address_id: int
    address_country: str
    address_zip_code: str
    address_state: str
    address_city: str
    address_neighborhood: str
    address_street: str
    address_number: str
    address_complement: str | None = None
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class AddressCreateSchema(BaseModel):
    address_country: str
    address_zip_code: str
    address_state: str
    address_city: str
    address_neighborhood: str
    address_street: str
    address_number: str
    address_complement: str | None = None
