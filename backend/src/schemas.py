from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


# retorna apenas o usuário e email, sem a senha
class UserPublic(BaseModel):
    username: str
    email: EmailStr
    userId: int


class UserDB(UserSchema):
    userId: int


class UserList(BaseModel):
    users: list[UserPublic]
