# from pydantic import BaseModel, EmailStr


# class Message(BaseModel):
#     message: str


# class UserSchema(BaseModel):
#     user_name: str
#     user_nickname: str
#     user_email: EmailStr
#     user_password: str


# class UserPublic(BaseModel):
#     user_id: int
#     user_name: str
#     user_nickname: str
#     user_email: EmailStr


# class UserDB(UserSchema):
#     user_id: int


# class UserList(BaseModel):
#     users: list[UserPublic]
