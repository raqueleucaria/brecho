from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.model.user import User
from src.schema.authSchema import Token
from src.security import create_access_token, verify_password

router = APIRouter(prefix='/auth', tags=['auth'])

OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
Session = Annotated[AsyncSession, Depends(get_session)]


# aqui é feita uma requisição ao banco,
# como o banco é assncrono agora é necessario add async
# e o uso de await para as operações de banco de dados
@router.post('/token/', response_model=Token)
async def login(form_data: OAuth2Form, session: Session):
    user = await session.scalar(
        select(User).where(User.user_email == form_data.username)
    )
    if not user or not verify_password(form_data.password, user.user_password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail='Invalid credentials'
        )
    access_token = create_access_token(data={'sub': user.user_email})
    return {'access_token': access_token, 'token_type': 'bearer'}
