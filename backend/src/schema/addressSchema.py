from pydantic import BaseModel, constr


class AddressSchema(BaseModel):
    address_country: str
    address_zip_code: str
    address_state: str
    address_city: str
    address_neighborhood: str
    address_street: str
    address_number: constr(min_length=1, max_length=5, pattern=r'^\d+$')
    address_complement: str | None = None


class AddressPublic(AddressSchema):
    address_id: int


class AddressList(AddressPublic):
    addresses: list[AddressPublic]


class AddressUpdate(AddressSchema):
    address_country: str | None = None
    address_zip_code: str | None = None
    address_state: str | None = None
    address_city: str | None = None
    address_neighborhood: str | None = None
    address_street: str | None = None
    address_number: (
        constr(min_length=1, max_length=5, pattern=r'^\d+$') | None
    ) = None
    address_complement: str | None = None
