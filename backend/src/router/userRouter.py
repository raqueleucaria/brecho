from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.models import User
from src.schemas import (
    FilterPage,
    Message,
    UserList,
    UserPublic,
    UserSchema,
)
from src.security import (
    get_current_user,
    get_password_hash,
)

router = APIRouter(prefix='/user', tags=['user'])

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get('/', response_model=UserList)
async def read_users(
        session: Session,
        filter_users: Annotated[FilterPage, Query()]
    ):
    users = await session.scalars(
        select(User).offset(filter_users.offset).limit(filter_users.limit)
    )
    users = users.all()
    return {'users': users}


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(user: UserSchema, session: Session):
    db_user = await session.scalar(
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
    await session.commit()
    await session.refresh(db_user)

    return db_user


@router.put('/{user_id}', response_model=UserPublic)
async def update_user(
    user_id: int,
    user: UserSchema,
    session: Session,
    current_user: CurrentUser,
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
        await session.commit()
        await session.refresh(current_user)

        return current_user

    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Nickname or Email already exists',
        )


@router.delete('/{user_id}', response_model=Message)
async def delete_user(
    user_id: int,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    await session.delete(current_user)
    await session.commit()

    return {'message': 'User deleted'}
