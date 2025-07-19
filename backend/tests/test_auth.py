from http import HTTPStatus


def test_get_token(client, user):
    response = client.post(
        '/auth/token/',
        data={
            'username': user.user_email,
            'password': user.clear_password,
        },
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_login_invalid_credentials(client, user):
    response = client.post(
        '/auth/token/',
        data={
            'username': user.user_email,
            'password': 'wrongpassword',
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Invalid credentials'}
