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


def test_read_user(client):
    response = client.get('/user/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/user/')
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/user/1',
        json={
            'user_name': 'user_updated',
            'user_nickname': 'user_updated_nick',
            'user_email': 'user_updated@example.com',
            'user_password': 'mynewpassword_updated',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'user_id': 1,
        'user_name': 'user_updated',
        'user_nickname': 'user_updated_nick',
        'user_email': 'user_updated@example.com',
    }


def test_update_integrity_error(client, user):
    client.post(
        '/user/',
        json={
            'user_name': 'user_repeated',
            'user_nickname': 'usernick_repeated_nick',
            'user_email': 'user_repeated@example.com',
            'user_password': 'secret',
        },
    )

    response_update = client.put(
        f'/user/{user.user_id}',
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


def test_update_user_not_found(client):
    response = client.put(
        '/user/999',
        json={
            'user_name': 'user_not_found',
            'user_nickname': 'nick_not_found',
            'user_email': 'ser_not_found@example.com',
            'user_password': 'notfoundpassword',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user):
    response = client.delete('/user/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client):
    response = client.delete('/user/999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
