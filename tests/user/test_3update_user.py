from http import HTTPStatus


def test_update_user_deve_retornar_ok_e_usuario_atualizado(client):
    response = client.put(
        '/users/1',
        json={
            'organizacaoId': 2,
            'eNaoGovernamental': False,
            'eGerente': False,
            'primeiroNome': 'João',
            'sobrenome': 'Lira',
            'email': 'eduardolirainfo2@gmail.com',
            'telefone': '61999999999',
            'dataNascimento': '1990-01-01',
            'eSurdo': False,
            'usaCadeiraDeRodas': False,
            'temDeficienciaCognitiva': False,
            'eLgbtq': False,
            'urlImagemPerfil': 'https://avatars.githubusercontent.com/u/4684754?v=4',
            'senhaHash': '123456',
            'favoritos': [],
            'criadoEm': '2021-01-01T00:00:00',
            'atualizadoEm': '2021-01-01T00:00:00',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'organizacaoId': 2,
        'eNaoGovernamental': False,
        'eGerente': False,
        'primeiroNome': 'João',
        'sobrenome': 'Lira',
        'email': 'eduardolirainfo2@gmail.com',
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


def test_update_user_deve_retornar_not_found_quando_usuario_nao_existe(client):
    user_id_invalido = 999
    response = client.put(
        f'/users/{user_id_invalido}',
        json={
            'organizacaoId': 2,
            'eNaoGovernamental': False,
            'eGerente': False,
            'primeiroNome': 'João',
            'sobrenome': 'Lira',
            'email': 'eduardolirainfo2@gmail.com',
            'telefone': '61999999999',
            'dataNascimento': '1990-01-01',
            'eSurdo': False,
            'usaCadeiraDeRodas': False,
            'temDeficienciaCognitiva': False,
            'eLgbtq': False,
            'urlImagemPerfil': 'https://avatars.githubusercontent.com/u/4684754?v=4',
            'senhaHash': '123456',
            'favoritos': [],
            'criadoEm': '2021-01-01T00:00:00',
            'atualizadoEm': '2021-01-01T00:00:00',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário não encontrado'}
