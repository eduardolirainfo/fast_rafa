from http import HTTPStatus


def test_delete_user_deve_retornar_no_content_e_usuario_deletado(client):
    response = client.delete('/users/1')
    assert response.json() == {'message': 'Usuário deletado com sucesso'}


def test_delete_user_deve_retornar_not_found_quando_usuario_nao_existe(client):
    response = client.delete('/users/999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário não encontrado'}
