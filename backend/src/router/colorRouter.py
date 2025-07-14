from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.repository.colorRepository import ColorRepository
from src.schema.colorSchema import ColorList, ColorSchema
from src.schema.filterSchema import FilterPage

router = APIRouter(prefix='/color', tags=['color'])
Session = Annotated[AsyncSession, Depends(get_session)]


@router.get('/', response_model=ColorList)
async def get_all_colors(
    session: Session, pagination: Annotated[FilterPage, Query()]
):
    colors = await ColorRepository.get_all_colors(
        session, pagination.offset, pagination.limit
    )
    return {'colors': colors}


@router.get('/{color_id}', response_model=ColorSchema)
async def get_color_by_id(color_id: int, session: Session):
    color = await ColorRepository.get_by_id(session, color_id)
    if not color:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Color not found.'
        )
    return color


@router.get('/{color_name}', response_model=ColorSchema)
async def get_color_by_name(color_name: str, session: Session):
    decoded_name = color_name.replace('%20', ' ')

    color = await ColorRepository.get_by_name(session, decoded_name)

    if not color:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Color with name '{decoded_name}' not found.",
        )

    return color
