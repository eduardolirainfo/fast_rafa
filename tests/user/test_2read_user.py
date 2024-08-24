from http import HTTPStatus


def test_read_user_deve_retornar_ok_e_usuario(client):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
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
    }


def test_read_user_deve_retornar_not_found_quando_usuario_nao_existe(client):
    user_id_invalido = 999
    response = client.get(f'/users/{user_id_invalido}')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário não encontrado'}
