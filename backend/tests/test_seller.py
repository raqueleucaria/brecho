from http import HTTPStatus

from src.schema.sellerSchema import SellerPublic


def test_create_seller(client, token, user):
    response = client.post(
        '/seller/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'seller_description': 'Test Seller',
            'seller_status': 'inactive',
            'seller_bank_account': '1234567',
            'seller_bank_agency': '1234',
            'seller_bank_name': 'Test Bank',
            'seller_bank_type': 'checking',
            'user_id': user.user_id,
        },
    )
    assert response.json() == {
        'seller_id': 1,
        'seller_description': 'Test Seller',
        'seller_status': 'inactive',
    }


def test_create_seller_conflict(client, token, user):
    client.post(
        '/seller/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'seller_description': 'Test Seller',
            'seller_status': 'inactive',
            'seller_bank_account': '1234567',
            'seller_bank_agency': '1234',
            'seller_bank_name': 'Test Bank',
            'seller_bank_type': 'checking',
            'user_id': user.user_id,
        },
    )

    response = client.post(
        '/seller/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'seller_description': 'Test Seller Again',
            'seller_status': 'active',
            'seller_bank_account': '7654321',
            'seller_bank_agency': '4321',
            'seller_bank_name': 'Another Bank',
            'seller_bank_type': 'savings',
            'user_id': user.user_id,
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        'detail': 'Seller profile already exists for this user'
    }


def test_read_sellers(client, seller):
    seller_schema = SellerPublic.model_validate(seller).model_dump()
    seller_schema['seller_status'] = (
        seller_schema['seller_status'].value
        if hasattr(seller_schema['seller_status'], 'value')
        else seller_schema['seller_status']
    )
    response = client.get('/seller/')
    assert response.json() == {'sellers': [seller_schema]}


def test_update_seller(client, token, seller):
    response = client.put(
        f'/seller/{seller.seller_id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'seller_description': 'Updated Description',
            'seller_bank_account': '7654321',
            'seller_bank_agency': '4321',
            'seller_bank_name': 'Updated Bank',
            'seller_bank_type': 'savings',
            'seller_status': 'active',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'seller_id': seller.seller_id,
        'seller_description': 'Updated Description',
        'seller_bank_account': '7654321',
        'seller_bank_agency': '4321',
        'seller_bank_name': 'Updated Bank',
        'seller_bank_type': 'savings',
        'seller_status': 'active',
    }


def test_update_seller_forbidden(client, other_seller, token):
    response = client.put(
        f'/seller/{other_seller.seller_id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'seller_description': 'Updated Description',
            'seller_bank_account': '7654321',
            'seller_bank_agency': '4321',
            'seller_bank_name': 'Updated Bank',
            'seller_bank_type': 'savings',
            'seller_status': 'active',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail': 'You do not have permission to update this seller profile'
    }


def test_update_seller_not_found(client, token):
    response = client.put(
        '/seller/999',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'seller_description': 'Updated Description',
            'seller_bank_account': '7654321',
            'seller_bank_agency': '4321',
            'seller_bank_name': 'Updated Bank',
            'seller_bank_type': 'savings',
            'seller_status': 'active',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Seller not found'}
