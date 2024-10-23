from datetime import datetime

from sqlalchemy import select

from fast_rafa.models.organization import Organization as OrganizationModel
from fast_rafa.models.user import User


def test_create_organization(session):
    organization = OrganizationModel(
        id_federal='12345678901',
        nao_governamental=True,
        url_logo='https://example.com/logo.jpg',
        url_imagem='https://example.com/image.jpg',
        abertura='08:00',
        fechamento='18:00',
        intervalo='12:00-13:00',
        nome='ONG',
        descricao='Organização não governamental',
        rua='Rua das ONGs',
        cep='12345-678',
        cidade='São Paulo',
        estado='SP',
        telefone='(11) 99999-9999',
        email='eduardolirainfO@gmail.com',
    )
    session.add(organization)
    session.commit()
    # session.refresh(organization)
    result = session.scalar(
        select(OrganizationModel).where(
            OrganizationModel.id_federal == '12345678901'
        )
    )
    assert result.nome == 'ONG'


def test_create_user(session):
    user = User(
        id_organizacao=1,
        nao_governamental=False,
        administrador=True,
        primeiro_nome='Eduardo',
        ultimo_nome='Lira',
        email='eduardolirainfo@gmail.com',
        telefone='(11) 99999-9999',
        data_nascimento=datetime.strptime('1980-01-01', '%Y-%m-%d').date(),
        deficiencia_auditiva=False,
        usa_cadeira_rodas=False,
        deficiencia_cognitiva=False,
        lgbtq=False,
        image_url_perfil='https://example.com/image.jpg',
        senha_hash='12345',
    )
    session.add(user)
    session.commit()
    result = session.scalar(
        select(User).where(User.email == 'eduardolirainfo@gmail.com')
    )
    assert result.primeiro_nome == 'Eduardo'
