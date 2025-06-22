from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    user_name: str
    user_nickname: str
    user_email: EmailStr
    user_password: str


class UserPublic(BaseModel):
    user_id: int
    user_name: str
    user_nickname: str
    user_email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]
