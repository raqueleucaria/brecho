from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.repository.categoryRepository import CategoryRepository
from src.schema.categorySchema import (
    CategoryList,
    CategoryPublic,
)

router = APIRouter(prefix='/category', tags=['category'])
Session = Annotated[AsyncSession, Depends(get_session)]


@router.get('/', response_model=CategoryList)
async def get_all_categories(session: Session):
    categories = await CategoryRepository.get_categories(session)
    return {'categories': categories}


@router.get('/{category_id}', response_model=CategoryPublic)
async def get_category_by_id(category_id: int, session: Session):
    category = await CategoryRepository.get_category_by_id(
        session, category_id
    )
    if not category:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return CategoryPublic.model_validate(category)


@router.get('/name/{category_name}', response_model=CategoryPublic)
async def get_category_by_name(category_name: str, session: Session):
    decoded_name = category_name.replace('%20', ' ')

    category = await CategoryRepository.get_by_name(session, decoded_name)

    if not category:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Category with name '{decoded_name}' not found.",
        )

    return category
