from pydantic import BaseModel, ConfigDict, Field

from src.model.seller import BankType, SellerStatus


class SellerSchema(BaseModel):
    seller_description: str = Field(..., max_length=500)
    seller_bank_account: str = Field(..., max_length=7)
    seller_bank_agency: str = Field(..., max_length=6)
    seller_bank_name: str = Field(..., max_length=100)
    seller_bank_type: BankType
    seller_status: SellerStatus = Field(
        default=SellerStatus.inactive,
        description='Status of the seller profile',
    )

    # model_config = ConfigDict(from_attributes=True)


class SellerPublic(BaseModel):
    seller_id: int
    seller_description: str = Field(..., max_length=500)
    seller_status: SellerStatus = Field(
        default=SellerStatus.inactive,
        description='Status of the seller profile',
    )
    model_config = ConfigDict(from_attributes=True)


class SellerPrivate(SellerPublic):
    seller_id: int
    seller_description: str = Field(..., max_length=500)
    seller_bank_account: str = Field(..., max_length=7)
    seller_bank_agency: str = Field(..., max_length=6)
    seller_bank_name: str = Field(..., max_length=100)
    seller_bank_type: BankType
    seller_status: SellerStatus = Field(
        default=SellerStatus.inactive,
        description='Status of the seller profile',
    )
    model_config = ConfigDict(from_attributes=True)


class SellerList(BaseModel):
    sellers: list[SellerPublic]
