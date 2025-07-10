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
