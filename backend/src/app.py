from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.database import get_session
from src.models import User
from src.schemas import Message, Token, UserList, UserPublic, UserSchema
from src.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)

app = FastAPI(
    title='Brechó',
    description=(
        'Brechó is an online thrift store API with user authentication, store '
        'and product management, '
        'shopping cart, order tracking, and multiple payment options.'
    ),
    version='1.0.0',
)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Welcome to Brechó API!'}


@app.get('/user/', response_model=UserList)
def read_users(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


@app.post('/user/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.user_nickname == user.user_nickname)
            | (User.user_email == user.user_email)
        )
    )

    if db_user:
        if db_user.user_nickname == user.user_nickname:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Nickname already exists',
            )
        elif db_user.user_email == user.user_email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email already exists',
            )

    hashed_password = get_password_hash(user.user_password)

    db_user = User(
        user_name=user.user_name,
        user_nickname=user.user_nickname,
        user_email=user.user_email,
        user_password=hashed_password,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.put('/user/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    try:
        current_user.user_name = user.user_name
        current_user.user_nickname = user.user_nickname
        current_user.user_password = get_password_hash(user.user_password)
        current_user.user_email = user.user_email
        session.commit()
        session.refresh(current_user)

        return current_user

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Nickname or Email already exists',
        )


@app.delete('/user/{user_id}', response_model=Message)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted'}


@app.post('/token/', response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(
        select(User).where(User.user_email == form_data.username)
    )
    if not user or not verify_password(form_data.password, user.user_password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail='Invalid credentials'
        )
    access_token = create_access_token(data={'sub': user.user_email})
    return {'access_token': access_token, 'token_type': 'bearer'}
