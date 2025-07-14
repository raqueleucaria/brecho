from http import HTTPStatus

import pytest

from .factories import AddressFactory


def test_create_address(client, token):
    response = client.post(
        '/address/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'address_country': 'Brazil',
            'address_zip_code': '12345-678',
            'address_state': 'SP',
            'address_city': 'São Paulo',
            'address_neighborhood': 'Centro',
            'address_street': 'Rua Exemplo',
            'address_number': '123',
            'address_complement': 'Apto 456',
        },
    )
    assert response.json() == {
        'address_id': 1,
        'address_country': 'Brazil',
        'address_zip_code': '12345-678',
        'address_state': 'SP',
        'address_city': 'São Paulo',
        'address_neighborhood': 'Centro',
        'address_street': 'Rua Exemplo',
        'address_number': '123',
        'address_complement': 'Apto 456',
    }


@pytest.mark.asyncio
async def test_list_addresses_return_5(session, client, user, token):
    excepted_addresses = 5
    session.add_all(AddressFactory.create_batch(5, user_id=user.user_id))
    await session.commit()
    response = client.get(
        '/address/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert len(response.json()) == excepted_addresses


def test_update_address_error(client, token):
    response = client.patch(
        '/address/999',
        json={'address_country': 'Test'},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Address not found'}


@pytest.mark.asyncio
async def test_delete_address(session, client, user, token):
    address = AddressFactory(user_id=user.user_id)

    session.add(address)
    await session.commit()

    response = client.delete(
        f'/address/{address.address_id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Address deleted successfully'}


def test_delete_address_not_found(client, token):
    response = client.delete(
        '/address/999',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Address not found'}
