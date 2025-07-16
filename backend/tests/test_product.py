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
