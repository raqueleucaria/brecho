from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    user_name: str
    user_nickname: str
    user_email: EmailStr
    user_password: str
    user_phone_country_code: str
    user_phone_state_code: str
    user_phone_number: str


class UserPublic(BaseModel):
    user_id: int
    user_name: str
    user_nickname: str
    user_email: EmailStr
    user_phone_country_code: str
    user_phone_state_code: str
    user_phone_number: str
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class FilterPage(BaseModel):
    offset: int = 0
    limit: int = 100
