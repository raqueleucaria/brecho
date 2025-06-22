from http import HTTPStatus

from src.schemas import UserPublic


def test_root_returns_welcome_message(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Welcome to Brechó API!'}


def test_create_user(client):
    response = client.post(
        '/user/',
        json={
            'user_name': 'user1',
            'user_nickname': 'usernick1',
            'user_email': 'user1@example.com',
            'user_password': 'secret123',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'user_id': 1,
        'user_name': 'user1',
        'user_nickname': 'usernick1',
        'user_email': 'user1@example.com',
    }


def test_create_user_with_existing_nickname(client, user):
    response = client.post(
        '/user/',
        json={
            'user_name': 'user2',
            'user_nickname': user.user_nickname,
            'user_email': 'user2@example.com',
            'user_password': 'secret456',
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
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'user_id': user.user_id,
        'user_name': 'user_updated',
        'user_nickname': 'user_updated_nick',
        'user_email': 'user_updated@example.com',
    }


def test_update_integrity_error(client, user, token):
    client.post(
        '/user',
        json={
            'user_name': 'user_repeated',
            'user_nickname': 'usernick_repeated_nick',
            'user_email': 'user_repeated@example.com',
            'user_password': 'secret',
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


def test_get_token(client, user):
    response = client.post(
        '/token/',
        data={
            'username': user.user_email,
            'password': user.clear_password,
        },
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_update_user_forbidden(client, user, another_user, token):
    # Tenta atualizar outro usuário autenticado como 'user'
    response = client.put(
        f'/user/{another_user.user_id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'user_name': 'forbidden',
            'user_nickname': 'forbidden_nick',
            'user_email': 'forbidden@example.com',
            'user_password': 'forbiddenpass',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_delete_user_forbidden(client, user, another_user, token):
    # Tenta deletar outro usuário autenticado como 'user'
    response = client.delete(
        f'/user/{another_user.user_id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_login_invalid_credentials(client, user):
    response = client.post(
        '/token/',
        data={
            'username': user.user_email,
            'password': 'wrongpassword',
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Invalid credentials'}
