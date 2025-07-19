from http import HTTPStatus


def test_create_address(client, token, user):
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
            'user_id': user.user_id,
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'address_country': 'Brazil',
        'address_zip_code': '12345-678',
        'address_state': 'SP',
        'address_city': 'São Paulo',
        'address_neighborhood': 'Centro',
        'address_street': 'Rua Exemplo',
        'address_number': '123',
        'address_complement': 'Apto 456',
        'user_id': user.user_id,
        'address_id': 1,
    }


# def test_read_address(client, token):
#     responde = client.get(
#         '/address/',
#         headers={'Authorization': f'Bearer {token}'},
#     )
#     assert responde.json() == {'addresses': []}


# @pytest.mark.asyncio
# async def test_list_addresses(session, client, user, token):
#     """
#     Testa a listagem de endereços para o usuário logado.
#     """
#     # Arrange: Cria 5 endereços para o usuário.
#     expected_addresses = 5
#     # PADRONIZAÇÃO: Usa user=user para criar o batch.
#     addresses = AddressFactory.create_batch(expected_addresses, user=user)
#     session.add_all(addresses)
#     await session.commit()

#     # Act
#     response = client.get(
#         '/address/',
#         headers={'Authorization': f'Bearer {token}'},
#     )

#     # Assert
#     assert response.status_code == HTTPStatus.OK
#     # Nota: A asserção abaixo assume que sua API retorna uma lista direta.
#     # Se a resposta for um objeto como {'addresses': [...]}, mude para len(response.json()['addresses'])
#     assert len(response.json()) == expected_addresses


# def test_update_address_not_found(client, token):
#     response = client.patch(
#         '/address/999',
#         json={'address_country': 'Test'},
#         headers={'Authorization': f'Bearer {token}'},
#     )
#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {'detail': 'Address not found'}


# @pytest.mark.asyncio
# async def test_delete_address(session, client, token, user):
#     address = AddressFactory(user=user)
#     session.add(address)
#     await session.commit()

#     await session.refresh(address)

#     response = client.delete(
#         f'/address/{address.address_id}',  # Agora o ID existe.
#         headers={'Authorization': f'Bearer {token}'},
#     )

#     # Assert
#     assert response.status_code == HTTPStatus.OK
#     assert response.json() == {'message': 'Address deleted successfully'}


# def test_delete_address_not_found(client, token):
#     response = client.delete(
#         '/address/999',
#         headers={'Authorization': f'Bearer {token}'},
#     )
#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {'detail': 'Address not found'}
