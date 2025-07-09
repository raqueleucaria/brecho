from http import HTTPStatus

from src.schema.userSchema import UserPublic


def test_create_user(client):
    response = client.post(
        '/user/',
        json={
            'user_name': 'user1',
            'user_nickname': 'usernick1',
            'user_email': 'user1@example.com',
            'user_password': 'secret123',
            'user_phone_country_code': '+55',
            'user_phone_state_code': '11',
            'user_phone_number': '123456789',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'user_id': 1,
        'user_name': 'user1',
        'user_nickname': 'usernick1',
        'user_email': 'user1@example.com',
        'user_phone_country_code': '+55',
        'user_phone_state_code': '11',
        'user_phone_number': '123456789',
    }


def test_create_user_with_existing_nickname(client, user):
    response = client.post(
        '/user/',
        json={
            'user_name': 'user2',
            'user_nickname': user.user_nickname,
            'user_email': 'user2@example.com',
            'user_password': 'secret456',
            'user_phone_country_code': '+55',
            'user_phone_state_code': '11',
            'user_phone_number': '123456789',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Nickname already exists'}


def test_create_user_with_existing_email(client, user):
    response = client.post(
        '/user/',
        json={
            'user_name': 'user3',
            'user_nickname': 'usernick3',
            'user_email': user.user_email,
            'user_password': 'secret789',
            'user_phone_country_code': '+55',
            'user_phone_state_code': '11',
            'user_phone_number': '123456789',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


def test_read_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/user/')
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f'/user/{user.user_id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'user_name': 'user_updated',
            'user_nickname': 'user_updated_nick',
            'user_email': 'user_updated@example.com',
            'user_password': 'mynewpassword_updated',
            'user_phone_country_code': '+55',
            'user_phone_state_code': '11',
            'user_phone_number': '123456789',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'user_id': user.user_id,
        'user_name': 'user_updated',
        'user_nickname': 'user_updated_nick',
        'user_email': 'user_updated@example.com',
        'user_phone_country_code': '+55',
        'user_phone_state_code': '11',
        'user_phone_number': '123456789',
    }


def test_update_integrity_error(client, user, token):
    client.post(
        '/user',
        json={
            'user_name': 'user_repeated',
            'user_nickname': 'usernick_repeated_nick',
            'user_email': 'user_repeated@example.com',
            'user_password': 'secret',
            'user_phone_country_code': '+55',
            'user_phone_state_code': '11',
            'user_phone_number': '123456789',
        },
    )

    response_update = client.put(
        f'/user/{user.user_id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'user_name': 'user_repeated',
            'user_nickname': 'usernick_repeated_nick',
            'user_email': 'user_repeated@example.com',
            'user_password': 'secret',
            'user_phone_country_code': '+55',
            'user_phone_state_code': '11',
            'user_phone_number': '123456789',
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'Nickname or Email already exists'
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/user/{user.user_id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_update_user_with_wrong_user(client, other_user, token):
    response = client.put(
        f'/user/{other_user.user_id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'user_name': 'wrong_user',
            'user_nickname': 'wrong_nick',
            'user_email': 'wrong_email@email.com',
            'user_password': 'wrongpass',
            'user_phone_country_code': '+55',
            'user_phone_state_code': '11',
            'user_phone_number': '123456789',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_delete_user_with_wrong_user(client, other_user, token):
    response = client.delete(
        f'/user/{other_user.user_id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}
