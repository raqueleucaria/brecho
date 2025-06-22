from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.database import get_session
from src.models import User
from src.schemas import Message, UserList, UserPublic, UserSchema
from src.security import get_password_hash

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
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    db_user = session.scalar(select(User).where(User.user_id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    try:
        db_user.user_name = user.user_name
        db_user.user_nickname = user.user_nickname
        db_user.user_password = get_password_hash(user.user_password)
        db_user.user_email = user.user_email
        session.commit()
        session.refresh(db_user)

        return db_user

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Nickname or Email already exists',
        )


@app.delete('/user/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.user_id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    session.delete(db_user)
    session.commit()

    return {'message': 'User deleted'}
