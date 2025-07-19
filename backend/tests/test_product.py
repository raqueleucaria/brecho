from http import HTTPStatus

import pytest
from fastapi import HTTPException

from src.repository.productRepository import ProductRepository


def test_create_product(client, token, user, seller):
    user.seller_profile = seller
    response = client.post(
        '/product/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'product_name': 'Test Product',
            'product_price': 100.0,
            'product_description': 'This is a test product',
            'product_condition': 'new',
            'product_gender': 'U',
            'product_size': 'M',
            'category_id': 1,
            'color_id': 1,
            'seller_id': user.seller_profile.seller_id,
            'product_status': 'available',
        },
    )
    assert response.json() == {
        'product_name': 'Test Product',
        'product_price': 100.0,
        'product_description': 'This is a test product',
        'product_condition': 'new',
        'product_gender': 'U',
        'product_size': 'M',
        'category_id': 1,
        'color_id': 1,
        'product_status': 'available',
        'product_id': 1,
        'seller_id': user.seller_profile.seller_id,
    }


def test_read_products(client):
    response = client.get(
        '/product/',
    )
    assert response.json() == {'products': []}


def test_get_product_by_id(client, product):
    response = client.get(f'/product/{product.product_id}')
    assert response.json() == {
        'product_name': product.product_name,
        'product_price': float(product.product_price),
        'product_description': product.product_description,
        'product_condition': product.product_condition.value,
        'product_gender': product.product_gender.value,
        'product_size': product.product_size.value,
        'category_id': product.category_id,
        'color_id': product.color_id,
        'product_status': product.product_status.value,
        'product_id': product.product_id,
        'seller_id': product.seller_id,
    }


def test_get_product_not_found(client):
    response = client.get('/product/9999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Product not found'}


def test_delete_product(client, token, product, user, seller):
    user.seller_profile = seller
    response = client.delete(
        f'/product/{product.product_id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_product_forbidden(
    client, product, other_user, other_token, other_seller
):
    other_user.seller_profile = other_seller
    response = client.delete(
        f'/product/{product.product_id}',
        headers={'Authorization': f'Bearer {other_token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail': 'You do not have permission to delete this product'
    }


def test_delete_product_not_found(client, token):
    response = client.delete(
        '/product/9999',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Product not found'}


@pytest.mark.asyncio
async def test_delete_product_exception(session, product, mocker):
    mocker.patch.object(
        session, 'commit', side_effect=Exception('Error deleting product')
    )

    with pytest.raises(HTTPException) as exc_info:
        await ProductRepository.delete_product(session, product)

    assert exc_info.value.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


@pytest.mark.asyncio
async def test_path_product(client, product, user, token, seller):
    user.seller_profile = seller
    response = client.patch(
        f'/product/{product.product_id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'product_name': 'Updated Product'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['product_name'] == 'Updated Product'


def test_path_product_forbidden(
    client, product, other_user, other_token, other_seller
):
    other_user.seller_profile = other_seller
    response = client.patch(
        f'/product/{product.product_id}',
        headers={'Authorization': f'Bearer {other_token}'},
        json={'product_name': 'Updated Product'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail': 'You do not have permission to update this product'
    }


def test_path_product_not_found(client, token):
    response = client.patch(
        '/product/9999',
        headers={'Authorization': f'Bearer {token}'},
        json={'product_name': 'Updated Product'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Product not found'}
    assert response.json() == {'detail': 'Product not found'}


@pytest.mark.asyncio
async def test_update_product_no_data(client, token, user, product, seller):
    user.seller_profile = seller
    response = client.patch(
        f'/product/{product.product_id}',
        headers={'Authorization': f'Bearer {token}'},
        json={},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'No update data provided'}
