from http import HTTPStatus

from fastapi.testclient import TestClient

from src.app import app


def test_root_should_return_ok_and_hello_world():
    client = TestClient(app)  # Arrange

    response = client.get('/')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert

    assert response.json() == {'message': 'Hello World!!!'}  # Assert
