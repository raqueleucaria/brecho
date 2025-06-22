from http import HTTPStatus


def test_root_returns_welcome_message(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Welcome to Brechó API!'}
