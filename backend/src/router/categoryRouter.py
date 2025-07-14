from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.repository.categoryRepository import CategoryRepository
from src.schema.categorySchema import CategoryList, CategorySchema
from src.schema.filterSchema import FilterPage

router = APIRouter(prefix='/category', tags=['category'])
Session = Annotated[AsyncSession, Depends(get_session)]


@router.get('/', response_model=CategoryList)
async def get_all_categories(
    session: Session, pagination: Annotated[FilterPage, Query()]
):
    categories = await CategoryRepository.get_all_categories(
        session, pagination.offset, pagination.limit
    )
    return {'categories': categories}


@router.get('/{category_id}', response_model=CategorySchema)
async def get_category_by_id(category_id: int, session: Session):
    category = await CategoryRepository.get_by_id(session, category_id)
    if not category:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Category not found.'
        )
    return category


@router.get('/{category_name}', response_model=CategorySchema)
async def get_category_by_name(category_name: str, session: Session):
    decoded_name = category_name.replace('%20', ' ')

    category = await CategoryRepository.get_by_name(session, decoded_name)

    if not category:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Category with name '{decoded_name}' not found.",
        )

    return category
