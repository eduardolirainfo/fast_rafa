from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_rafa.app import app
from fast_rafa.database import get_session
from fast_rafa.models.base import table_registry
from fast_rafa.models.organization import Organization
from fast_rafa.models.user import User
from fast_rafa.schemas.user import CreateUser
from fast_rafa.security import get_password_hash


@pytest.fixture
def token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    table_registry.metadata.drop_all(engine)


@contextmanager
def _mock_db_time(*, model, time=datetime(2024, 1, 1)):
    def fake_time_handler(mapper, connection, target):
        if hasattr(target, 'criado_em'):
            target.created_at = time
        if hasattr(target, 'atualizado_em'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_handler)

    yield time

    event.remove(model, 'before_insert', fake_time_handler)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def organization(session):
    organization_data = Organization.CreateOrganization(
        id_federal='12345678901',
        nao_governamental=True,
        url_logo='https://example.com/logo.png',
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
        email='eduardolirainfo@gmail.com',
    )

    organization = Organization.create(organization_data)

    session.add(organization)
    session.commit()
    session.refresh(organization)

    return organization


@pytest.fixture
def user(session):
    pwd = '123456'
    user_data = CreateUser(
        id_organizacao=1,
        eh_voluntario=True,
        eh_gerente=True,
        primeiro_nome='Eduardo',
        sobrenome='Lira',
        email='eduardolirainfo@gmail.com',
        username='eduardolira',
        senha_hash=get_password_hash(pwd),
        telefone='(11) 99999-9999',
        deficiencia_auditiva=True,
        usa_cadeira_rodas=True,
        deficiencia_cognitiva=True,
        lgbtq=True,
        url_imagem_perfil='https://example.com/image.jpg',
    )

    user = User.create(user_data)
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = pwd  # Monkey patching

    return user
