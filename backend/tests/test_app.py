from http import HTTPStatus


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'user1',
            'email': 'user1@example.com',
            'password': 'secret123',
        },
    )  # Act

    assert response.status_code == HTTPStatus.CREATED  # Assert
    assert response.json() == {
        'username': 'user1',
        'email': 'user1@example.com',
        'userId': 1,
    }  # Assert


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'user1',
                'email': 'user1@example.com',
                'userId': 1,
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'user2',
            'email': 'user2@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'user2',
        'email': 'user2@example.com',
        'userId': 1,
    }


def test_update_user_not_found(client):
    response = client.put(
        '/users/999',
        json={
            'username': 'user1',
            'email': 'user1@example.com',
            'password': 'secret123',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client):
    response = client.delete('/users/999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
