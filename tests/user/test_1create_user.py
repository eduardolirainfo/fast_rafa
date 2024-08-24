from http import HTTPStatus


def test_create_user_deve_retornar_created_e_usuario_criado(client):
    response = client.post(
        '/users',
        json={
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
            'senhaHash': '123456',
            'favoritos': [],
            'criadoEm': '2021-01-01T00:00:00',
            'atualizadoEm': '2021-01-01T00:00:00',
        },
    )
    # voltou 201 created?
    assert response.status_code == HTTPStatus.CREATED
    # o usuário foi criado?
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
