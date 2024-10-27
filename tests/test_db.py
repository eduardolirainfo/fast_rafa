from sqlalchemy import select

from fast_rafa.models.organization import Organization as OrganizationModel


def test_create_organization(session):
    # Dados para criação da organização
    data = {
        'id_federal': '12345678901',
        'nao_governamental': True,
        'url_logo': 'https://example.com/logo.jpg',
        'url_imagem': 'https://example.com/image.jpg',
        'abertura': '08:00',
        'fechamento': '18:00',
        'intervalo': '12:00-13:00',
        'nome': 'ONG',
        'descricao': 'Organização não governamental',
        'rua': 'Rua das ONGs',
        'cep': '12345-678',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'telefone': '(11) 99999-9999',
        'email': 'eduardolirainfO@gmail.com',
    }

    organization_data = OrganizationModel.CreateOrganization(**data)
    organization = OrganizationModel.create(organization_data)

    session.add(organization)
    session.commit()
    session.refresh(organization)

    result = session.scalar(
        select(OrganizationModel).where(
            OrganizationModel.id_federal == '12345678901'
        )
    )

    assert (
        result is not None
    ), 'A organização não foi encontrada no banco de dados.'
    assert result.nome == 'ONG'
    assert result.id_federal == '12345678901'
    assert result.nao_governamental is True
    assert result.url_logo == 'https://example.com/logo.jpg'
    assert result.url_imagem == 'https://example.com/image.jpg'
    assert result.abertura == '08:00'
    assert result.fechamento == '18:00'
    assert result.intervalo == '12:00-13:00'
    assert result.descricao == 'Organização não governamental'
    assert result.rua == 'Rua das ONGs'
    assert result.cep == '12345-678'
    assert result.cidade == 'São Paulo'
    assert result.estado == 'SP'
    assert result.telefone == '(11) 99999-9999'
    assert result.email == 'eduardolirainfO@gmail.com'


def test_update_organization(session):
    initial_data = {
        'id_federal': '12345678901',
        'nao_governamental': True,
        'url_logo': 'https://example.com/logo.jpg',
        'url_imagem': 'https://example.com/image.jpg',
        'abertura': '08:00',
        'fechamento': '18:00',
        'intervalo': '12:00-13:00',
        'nome': 'ONG Inicial',
        'descricao': 'Descrição inicial da organização',
        'rua': 'Rua das ONGs',
        'cep': '12345-678',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'telefone': '(11) 99999-9999',
        'email': 'initial_email@gmail.com',
    }

    organization_data = OrganizationModel.CreateOrganization(**initial_data)
    organization = OrganizationModel.create(organization_data)

    update_data = {
        'id_federal': '12345678901',
        'nao_governamental': False,  # Mudando para False
        'url_logo': 'https://example.com/new_logo.jpg',
        'url_imagem': 'https://example.com/new_image.jpg',
        'abertura': '09:00',  # Mudando a abertura
        'fechamento': '17:00',  # Mudando o fechamento
        'intervalo': '12:30-13:30',
        'nome': 'ONG Atualizada',
        'descricao': 'Descrição atualizada da organização',
        'rua': 'Rua das ONGs Atualizada',
        'cep': '87654-321',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'telefone': '(11) 88888-8888',
        'email': 'updated_email@gmail.com',
    }

    organization = OrganizationModel.update(organization, update_data)

    assert organization.nao_governamental == update_data['nao_governamental']
    assert organization.url_logo == update_data['url_logo']
    assert organization.url_imagem == update_data['url_imagem']
    assert organization.abertura == update_data['abertura']
    assert organization.fechamento == update_data['fechamento']
    assert organization.intervalo == update_data['intervalo']
    assert organization.nome == update_data['nome']
    assert organization.descricao == update_data['descricao']
    assert organization.rua == update_data['rua']
    assert organization.cep == update_data['cep']
    assert organization.cidade == update_data['cidade']
    assert organization.estado == update_data['estado']
    assert organization.telefone == update_data['telefone']
    assert organization.email == update_data['email']


def test_delete_organization(session):
    # Dados para criar a organização
    data = {
        'id_federal': '12345678901',
        'nao_governamental': True,
        'url_logo': 'https://example.com/logo.jpg',
        'url_imagem': 'https://example.com/image.jpg',
        'abertura': '08:00',
        'fechamento': '18:00',
        'intervalo': '12:00-13:00',
        'nome': 'ONG a ser excluída',
        'descricao': 'Descrição da organização a ser excluída',
        'rua': 'Rua das ONGs',
        'cep': '12345-678',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'telefone': '(11) 99999-9999',
        'email': 'delete_email@gmail.com',
    }

    organization_data = OrganizationModel.CreateOrganization(**data)
    organization = OrganizationModel.create(organization_data)

    session.add(organization)
    session.commit()
    session.refresh(organization)

    assert organization.id is not None, \
        "ID da organização deve ser definido após a criação."

    session.delete(organization)
    session.commit()

    deleted_organization = (
        session.query(OrganizationModel)
        .filter(OrganizationModel.id == organization.id)
        .first()
    )

    if deleted_organization is None:
        delete_response = OrganizationModel.DeleteResponseOrganization(
            message="Organização excluída")
    else:
        delete_response = OrganizationModel.DeleteResponseOrganization(
            message="Falha ao excluir a organização")

    assert delete_response.message == "Organização excluída", \
        "Mensagem de sucesso não corresponde ao esperado."
