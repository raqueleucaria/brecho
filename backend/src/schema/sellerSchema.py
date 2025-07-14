from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from src.model.seller import BankType, SellerStatus


class SellerCreate(BaseModel):
    seller_description: Optional[str] = Field(None, max_length=500)
    seller_bank_account: str = Field(
        ..., max_length=20, description='Number of the bank account'
    )
    seller_bank_agency: str = Field(
        ..., max_length=10, description='Agency number of the bank account'
    )
    seller_bank_name: str = Field(..., max_length=100)
    seller_bank_type: BankType


class SellerUpdate(BaseModel):
    seller_description: Optional[str] = Field(None, max_length=500)
    seller_bank_account: Optional[str] = Field(None, max_length=20)
    seller_bank_agency: Optional[str] = Field(None, max_length=10)
    seller_bank_name: Optional[str] = Field(None, max_length=100)
    seller_bank_type: Optional[BankType] = None
    seller_status: Optional[SellerStatus] = None


class SellerPublic(BaseModel):
    seller_id: int
    seller_id: int
    seller_description: Optional[str]
    seller_status: SellerStatus
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class SellerPrivate(SellerPublic):
    seller_bank_account: str
    seller_bank_agency: str
    seller_bank_name: str
    seller_bank_type: BankType

    model_config = ConfigDict(from_attributes=True)


class SellerList(BaseModel):
    clients: list[SellerPublic]
