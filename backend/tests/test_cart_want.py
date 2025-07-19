from http import HTTPStatus

import pytest

from src.model.cart_want import WantType

# from fastapi import HTTPException

# from src.repository.productRepository import ProductRepository


def test_create_cart_want(client, token, client_profile, user, product):
    user.client_profile = client_profile
    response = client.post(
        '/cart-want/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'product_id': product.product_id,
            'want_type': WantType.cart.value,
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'product_id': product.product_id,
        'client_id': user.client_profile.client_id,
        'want_type': 'cart',
    }


def test_create_cart_want_with_nonexistent_product(
    client, token, client_profile, user
):
    user.client_profile = client_profile
    response = client.post(
        '/cart-want/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'product_id': 9999,
            'want_type': WantType.cart.value,
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Product not found'}


def test_list_cart_by_client_id(client, token, user, client_profile):
    user.client_profile = client_profile
    response = client.get(
        '/cart-want/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_update_cart_want(
    client, token, user, client_profile, cart_want
):
    user.client_profile = client_profile

    url = f'/cart-want/?product_id={cart_want.product_id}&client_id={
        cart_want.client_id
    }'
    response = client.patch(
        url,
        headers={'Authorization': f'Bearer {token}'},
        json={
            'want_type': WantType.wishlist.value,
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'product_id': cart_want.product_id,
        'client_id': cart_want.client_id,
        'want_type': 'wishlist',
    }


def test_delete_cart_want(client, token, user, client_profile, cart_want):
    user.client_profile = client_profile
    url = f'/cart-want/?product_id={cart_want.product_id}&client_id={
        cart_want.client_id
    }'
    response = client.delete(
        url,
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NO_CONTENT
