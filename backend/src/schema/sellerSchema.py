from pydantic import BaseModel, Field

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


class SellerList(BaseModel):
    sellers: list[SellerPublic]


# class SellerUpdate(BaseModel):
#     seller_description: Optional[str] = Field(None, max_length=500)
#     seller_bank_account: Optional[str] = Field(None, max_length=20)
#     seller_bank_agency: Optional[str] = Field(None, max_length=10)
#     seller_bank_name: Optional[str] = Field(None, max_length=100)
#     seller_bank_type: Optional[BankType] = None
#     seller_status: Optional[SellerStatus] = None


# class SellerPublic(BaseModel):
#     seller_id: int
#     seller_description: Optional[str]
#     seller_status: SellerStatus
#     user_id: int

#     model_config = ConfigDict(from_attributes=True)


# class SellerPrivate(SellerPublic):
#     seller_bank_account: str
#     seller_bank_agency: str
#     seller_bank_name: str
#     seller_bank_type: BankType

#     model_config = ConfigDict(from_attributes=True)


# class SellerList(BaseModel):
#     sellers: list[SellerPublic]
