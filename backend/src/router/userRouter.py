from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.model.user import User
from src.repository.clientRepository import ClientRepository
from src.repository.userRepository import UserRepository
from src.schema.filterSchema import FilterPage
from src.schema.messageSchema import Message
from src.schema.userSchema import (
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
    session: Session, filter_users: Annotated[FilterPage, Query()]
):
    users = await UserRepository.get_users(
        session, filter_users.offset, filter_users.limit
    )
    return {'users': users}


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(user: UserSchema, session: Session):
    db_user = await UserRepository.get_user_by_nickname_or_email(
        session, user.user_nickname, user.user_email
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

    try:
        hashed_password = get_password_hash(user.user_password)
        new_user = User(
            user_name=user.user_name,
            user_nickname=user.user_nickname,
            user_email=user.user_email,
            user_password=hashed_password,
            user_phone_country_code=user.user_phone_country_code,
            user_phone_state_code=user.user_phone_state_code,
            user_phone_number=user.user_phone_number,
        )

        create_user = await UserRepository.create_user(session, new_user)
        await ClientRepository.create_client_for_user(session, create_user)

        await session.commit()
        await session.refresh(create_user)

        return create_user

    except Expection:
        await session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail='An error occurred while creating the user',
        )


@router.put('/{user_id}', response_model=UserPublic)
async def update_user(
    user_id: int, user: UserSchema, session: Session, current_user: CurrentUser
):
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    user_data = {
        'user_name': user.user_name,
        'user_nickname': user.user_nickname,
        'user_password': get_password_hash(user.user_password),
        'user_email': user.user_email,
        'user_phone_country_code': user.user_phone_country_code,
        'user_phone_state_code': user.user_phone_state_code,
        'user_phone_number': user.user_phone_number,
    }

    try:
        return await UserRepository.update_user(
            session, current_user, user_data
        )
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Nickname or Email already exists',
        )


@router.delete('/{user_id}', response_model=Message)
async def delete_user(
    user_id: int, session: Session, current_user: CurrentUser
):
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    await UserRepository.delete_user(session, current_user)
    return {'message': 'User deleted'}
