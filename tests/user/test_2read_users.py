from http import HTTPStatus


def test_read_users_deve_retornar_ok_e_lista_de_usuarios(client):
    response = client.get('/users')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'organizacaoId': 1,
                'eNaoGovernamental': True,
                'eGerente': True,
                'primeiroNome': 'Eduardo',
                'sobrenome': 'Lira',
                'email': 'eduardolirainfo@gmail.com',
                'telefone': '61999999999',
                'dataNascimento': '1990-01-01',
                'eSurdo': False,
                'usaCadeiraDeRodas': False,
                'temDeficienciaCognitiva': False,
                'eLgbtq': False,
                'urlImagemPerfil': 'https://avatars.githubusercontent.com/u/4684754?v=4',
                'favoritos': [],
                'criadoEm': '2021-01-01T00:00:00',
                'atualizadoEm': '2021-01-01T00:00:00',
            },
        ],
    }
