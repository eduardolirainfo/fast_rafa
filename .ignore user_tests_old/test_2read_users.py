from http import HTTPStatus


def test_read_users_deve_retornar_ok_e_lista_de_usuarios(client):
    response = client.get('/users')

    assert response.status_code == HTTPStatus.OK
    response_data = response.json()

    expected_response = {
        'users': [
            {
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
            },
        ],
    }

    assert response_data == expected_response
