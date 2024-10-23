from http import HTTPStatus


def test_create_user_deve_retornar_created_e_usuario_criado(client):
    response = client.post(
        '/users',
        json={
            'id_organizacao': 1,
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
    assert response.status_code == HTTPStatus.CREATED

    response_data = response.json()

    # Verifica se `criadoem` e `atualizadoem` existem
    assert 'criadoem' in response_data
    assert 'atualizadoem' in response_data

    # Remove os campos `criadoem` e `atualizadoem` para comparar o restante
    del response_data['criadoem']
    del response_data['atualizadoem']

    expected_response = {
        'id_organizacao': 1,
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
        'id': 1,
    }
    assert response_data == expected_response
