import pytest

pytest.skip('Ignorado nos testes', allow_module_level=True)

# from http import HTTPStatus

# import pytest

# from src.model.cart_want import CartWant, WantType


# @pytest.mark.asyncio
# async def test_create_checkout_success(
#     session, client, token, client_profile, address, product, other_product
# ):
#     """
#     Teste do caminho feliz: cria um checkout com sucesso a partir de um carrinho com itens.
#     """
#     # Arrange: Configura o cenário
#     # 1. Cria um segundo produto para ter mais de um item no carrinho

#     # 2. Adiciona ambos os produtos ao carrinho do usuário
#     session.add_all([
#         CartWant(
#             client_id=client_profile.client_id,
#             product_id=product.product_id,
#             want_type=WantType.cart,
#         ),
#         CartWant(
#             client_id=client_profile.client_id,
#             product_id=other_product.product_id,
#             want_type=WantType.cart,
#         ),
#     ])
#     await session.commit()

#     # Act: Faz a chamada à API para criar o checkout
#     response = client.post(
#         '/checkout/',
#         headers={'Authorization': f'Bearer {token}'},
#         json={'address_id': address.address_id, 'promotion': 10.0},
#     )

#     # Assert: Verifica se a resposta está correta
#     assert response.status_code == HTTPStatus.CREATED

#     data = response.json()
#     assert data['client_id'] == client_profile.client_id
#     assert data['promotion'] == 10.0
#     assert sorted(data['product_ids']) == sorted([
#         product.product_id,
#         other_product.product_id,
#     ])

#     # Verifica se o total foi calculado corretamente (produtos + frete - promoção)
#     expected_total = (
#         float(product.product_price)
#         + float(other_product.product_price)
#         + 15.00  # Frete fixo do modelo Checkout
#         - 10.00
#     )
#     assert data['total_value'] == expected_total

#     # Verifica o efeito colateral: o carrinho do usuário deve estar vazio
#     cart_items_after = (
#         session.execute(
#             select(CartWant).where(
#                 CartWant.client_id == client_profile.client_id
#             )
#         )
#         .scalars()
#         .all()
#     )
#     assert len(cart_items_after) == 0


# def test_create_checkout_cart_is_empty(
#     client, token, user, client_profile, address
# ):
#     """Testa a falha ao tentar criar um checkout com o carrinho vazio."""
#     # Arrange: Garante que o usuário e o endereço existem, mas o carrinho está vazio

#     # Act
#     response = client.post(
#         '/checkout/',
#         headers={'Authorization': f'Bearer {token}'},
#         json={'address_id': address.address_id},
#     )

#     # Assert
#     assert response.status_code == HTTPStatus.BAD_REQUEST
#     assert response.json() == {'detail': 'Cart is empty'}


# def test_create_checkout_invalid_address(
#     client, token, user, client_profile, other_address
# ):
#     """Testa a falha ao tentar usar um endereço que não pertence ao usuário."""
#     # Arrange: 'other_address' pertence ao 'other_user'

#     # Act
#     response = client.post(
#         '/checkout/',
#         headers={'Authorization': f'Bearer {token}'},
#         json={
#             'address_id': other_address.address_id
#         },  # Tenta usar o endereço de outro usuário
#     )

#     # Assert
#     assert response.status_code == HTTPStatus.FORBIDDEN
#     assert response.json() == {'detail': 'Invalid address selected'}


# def test_get_checkout_details_success(
#     session, client, token, user, client_profile, address, product
# ):
#     """Testa a busca de um checkout existente, verificando o cálculo do valor."""
#     # Arrange: Cria um checkout manualmente para poder buscá-lo
#     checkout = Checkout(
#         client_id=client_profile.client_id,
#         promotion=5.0,
#     )
#     session.add(checkout)
#     session.commit()  # Commit para gerar o checkout_id

#     generate = Generate(
#         checkout_id=checkout.checkout_id, product_id=product.product_id
#     )
#     session.add(generate)
#     session.commit()

#     # Act: Busca o checkout recém-criado
#     response = client.get(
#         f'/checkout/{checkout.checkout_id}',
#         headers={'Authorization': f'Bearer {token}'},
#     )

#     # Assert
#     assert response.status_code == HTTPStatus.OK
#     data = response.json()
#     assert data['checkout_id'] == checkout.checkout_id

#     # Verifica se o cálculo on-the-fly está correto
#     expected_total = float(product.product_price) + 15.00 - 5.00
#     assert data['total_value'] == expected_total


# def test_get_checkout_details_forbidden(client, other_token, checkout):
#     """Testa se um usuário não pode ver o checkout de outro."""
#     # Arrange: A fixture 'checkout' cria um checkout para o 'user' principal.
#     # Usamos o 'other_token' para tentar acessá-lo.

#     # Act
#     response = client.get(
#         f'/checkout/{checkout.checkout_id}',
#         headers={'Authorization': f'Bearer {other_token}'},
#     )

#     # Assert
#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {'detail': 'Checkout not found'}
