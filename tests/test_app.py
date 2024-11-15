from http import HTTPStatus


def test_get_token(client, organization, user):
    print(user.username)
    print(user.clean_password)
    response = client.post(
        'auth/token',
        data={
            'username': user.username,
            'password': user.clean_password,
        },
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token
