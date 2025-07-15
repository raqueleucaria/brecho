from http import HTTPStatus


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


# @pytest.mark.asyncio
# async def test_list_all_sellers(session, client, user, other_user):
#     excepted_sellers = 2
#     sellers_user = SellerFactory(user_id=user.user_id)
#     sellers_other_user = SellerFactory(user_id=other_user.user_id)

#     session.add_all([sellers_user, sellers_other_user])
#     await session.commit()
#     response = client.get('/seller/')
#     assert response.status_code == HTTPStatus.OK
#     response_data = response.json()

#     assert 'sellers' in response_data
#     assert len(response_data['sellers']) == excepted_sellers


# @pytest.mark.asyncio
# async def test_get_seller_by_id(client, seller):
#     response = client.get(f'/seller/{seller.seller_id}')
#     assert response.status_code == HTTPStatus.OK
#     return seller


# @pytest.mark.asyncio
# async def test_get_seller_by_id_not_found(client):
#     response = client.get('/seller/999')
#     assert response.status_code == HTTPStatus.NOT_FOUND


# # @pytest.mark.asyncio
# # async def test_get_seller_by_user_id(client, seller, token):
# #     response = client.get(
# #         f'/seller/me/{seller.user_id}',
# #         headers={'Authorization': f'Bearer {token}'},
# #     )

# #     assert response.status_code == HTTPStatus.OK
# #     return seller


# @pytest.mark.asyncio
# async def test_seller_by_user_id_not_found(client, token):
#     response = client.get(
#         '/seller/me/999',
#         headers={'Authorization': f'Bearer {token}'},
#     )
#     assert response.status_code == HTTPStatus.NOT_FOUND


# # @pytest.mark.asyncio
# # async def test_get_my_seller_by_user_id_forbidden(client, token, other_user):
# #     response = client.get(
# #         f'/seller/me/{other_user.user_id}',
# #         headers={'Authorization': f'Bearer {token}'},
# #     )
# #     assert response.status_code == HTTPStatus.FORBIDDEN


# def test_create_seller(client, token, user, seller):
#     response = client.post(
#         '/seller/',
#         headers={'Authorization': f'Bearer {token}'},
#         json={
#             'seller_description': 'Test Seller',
#             'seller_status': 'inactive',
#             'seller_bank_account': '123456789',
#             'seller_bank_agency': '1234',
#             'seller_bank_name': 'Test Bank',
#             'seller_bank_type': 'checking',
#             'user_id': user.user_id,
#         },
#     )

#     assert response.status_code == HTTPStatus.CREATED
#     assert response.json() == {
#         'seller_id': 2,
#         'seller_description': 'Test Seller',
#         'seller_status': 'inactive',
#         'seller_bank_account': '123456789',
#         'seller_bank_agency': '1234',
#         'seller_bank_name': 'Test Bank',
#         'seller_bank_type': 'checking',
#         'user_id': user.user_id,
#     }


# def test_update_seller_error(client, token):
#     response = client.patch(
#         '/seller/me/999',
#         json={'seller_description': 'Updated Description'},
#         headers={'Authorization': f'Bearer {token}'},
#     )
#     assert response.status_code == HTTPStatus.NOT_FOUND


# def test_update_seller_forbidden(client, token, other_user):
#     response = client.patch(
#         '/seller/me/999',
#         json={'seller_description': 'Updated Description'},
#         headers={'Authorization': f'Bearer {token}'},
#     )
