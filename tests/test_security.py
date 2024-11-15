from http import HTTPStatus

from jwt import decode

from fast_rafa.security import ALGORITHM, SECRET_KEY, create_access_token


def test_jwt_token(client):
    data = {'sub': 'eduardolira'}
    token = create_access_token(data)

    decoded = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded['sub'] == data['sub']
    assert decoded['exp']


def test_jwt_invalid_token(client):
    response = client.delete(
        '/api/v1/users/1',
        headers={'Authorization': 'Bearer token-invalido'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Credenciais inválidas'}
