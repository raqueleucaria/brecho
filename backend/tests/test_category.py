from http import HTTPStatus

import pytest

from .factories import CategoryFactory


@pytest.mark.asyncio
async def test_list_all_categories(session, client):
    expected_categories = 2
    categories = [CategoryFactory(), CategoryFactory()]

    session.add_all(categories)
    await session.commit()

    response = client.get('/category/')
    assert response.status_code == HTTPStatus.OK
    response_data = response.json()

    assert 'categories' in response_data
    assert len(response_data['categories']) == expected_categories


@pytest.mark.asyncio
async def test_get_category_by_id(client, category):
    response = client.get(f'/category/{category.category_id}')
    assert response.status_code == HTTPStatus.OK
    return category


@pytest.mark.asyncio
async def test_get_category_by_name(session, client):
    category = CategoryFactory(category_name='Test Category')
    session.add(category)
    await session.commit()
    await session.refresh(category)

    # CORREÇÃO: Use a nova rota '/category/name/...'
    response = client.get('/category/name/Test%20Category')

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['category_name'] == 'Test Category'


@pytest.mark.asyncio
async def test_get_category_by_name_not_found(client):
    response = client.get('/category/name/Nonexistent%20Category')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert (
        response.json()['detail']
        == "Category with name 'Nonexistent Category' not found."
    )
