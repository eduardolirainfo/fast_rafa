from http import HTTPStatus


def test_update_user_deve_retornar_ok_e_usuario_atualizado(client):
    response = client.put(
        '/users/1',
        json={
            'id_organizacao': 2,
            'naogovernamental': True,
            'gerente': True,
            'primeironome': 'Eduardo',
            'sobrenome': 'Lira',
            'email': 'edduardolirainfo@gmail.com',
            'telefone': '21999999999',
            'datanascimento': '2024-09-02',
            'deficienciaauditiva': True,
            'usacadeirarodas': True,
            'deficienciacognitiva': True,
            'lgbtq': True,
            'urlimagemperfil': 'https://avatars.githubusercontent.com/u/4684754?v=4',
            'senhahash': '123456',
            'favoritos': [],
        },
    )

    print('xxx response.json()', response.json())

    assert response.status_code == HTTPStatus.OK

    response_data = response.json()

    assert 'senhahash' in response_data
    del response_data['senhahash']

    assert response_data == {
        'id_organizacao': 2,
        'naogovernamental': True,
        'gerente': True,
        'primeironome': 'Eduardo',
        'sobrenome': 'Lira',
        'email': 'edduardolirainfo@gmail.com',
        'telefone': '21999999999',
        'datanascimento': '2024-09-02',
        'deficienciaauditiva': True,
        'usacadeirarodas': True,
        'deficienciacognitiva': True,
        'lgbtq': True,
        'urlimagemperfil': 'https://avatars.githubusercontent.com/u/4684754?v=4',
        'favoritos': [],
    }


def test_update_user_deve_retornar_not_found_quando_usuario_nao_existe(client):
    response = client.put(
        '/users/999',
        json={
            'id_organizacao': 2,
            'naogovernamental': True,
            'gerente': True,
            'primeironome': 'Eduardo',
            'sobrenome': 'Lira',
            'email': 'edduardolirainfo@gmail.com',
            'telefone': '21999999999',
            'datanascimento': '2024-09-02',
            'deficienciaauditiva': True,
            'usacadeirarodas': True,
            'deficienciacognitiva': True,
            'lgbtq': True,
            'urlimagemperfil': 'https://avatars.githubusercontent.com/u/4684754?v=4',
            'senhahash': '123456',
            'favoritos': [],
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário não encontrado'}
