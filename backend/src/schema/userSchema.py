from pydantic import BaseModel, ConfigDict, EmailStr


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
