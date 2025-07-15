from http import HTTPStatus

import pytest

from .factories import ColorFactory


@pytest.mark.asyncio
async def test_list_all_colors(session, client):
    expected_colors = 2
    colors = [ColorFactory(), ColorFactory()]

    session.add_all(colors)
    await session.commit()

    response = client.get('/color/')
    assert response.status_code == HTTPStatus.OK
    response_data = response.json()

    assert 'colors' in response_data
    assert len(response_data['colors']) == expected_colors


@pytest.mark.asyncio
async def test_get_color_by_id(client, color):
    response = client.get(f'/color/{color.color_id}')
    assert response.status_code == HTTPStatus.OK
    return color


@pytest.mark.asyncio
async def test_get_color_by_name(session, client):
    color = ColorFactory(color_name='Test Color')
    session.add(color)
    await session.commit()
    await session.refresh(color)

    # CORREÇÃO: Use a nova rota '/color/name/...'
    response = client.get('/color/name/Test%20Color')

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['color_name'] == 'Test Color'


@pytest.mark.asyncio
async def test_get_color_by_name_not_found(client):
    response = client.get('/color/name/Nonexistent%20Color')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert (
        response.json()['detail']
        == "Color with name 'Nonexistent Color' not found."
    )
