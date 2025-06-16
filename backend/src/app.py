from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from src.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI(
    title='Brechó',
    description=(
        'Brechó is an online thrift store API with user authentication, store '
        'and product management, '
        'shopping cart, order tracking, and multiple payment options.'
    ),
    version='1.0.0',
)

database = []


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    # breakpoint() for debugging
    user_with_id = UserDB(**user.model_dump(), userId=len(database) + 1)
    database.append(user_with_id)
    return user_with_id


@app.get('/users/', response_model=UserList)
def read_users():
    return {'users': database}


@app.put('/users/{userId}', response_model=UserPublic)
def update_user(userId: int, user: UserSchema):
    if userId > len(database) or userId < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    user_with_id = UserDB(**user.model_dump(), userId=userId)
    database[userId - 1] = user_with_id

    return user_with_id


@app.delete('/users/{userId}', response_model=Message)
def delete_user(userId: int):
    if userId > len(database) or userId < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    del database[userId - 1]

    return {'message': 'User deleted'}
