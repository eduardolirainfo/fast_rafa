from random import choice

from faker import Faker
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from fast_rafa.models.organization import Organization
from fast_rafa.models.user import User
from fast_rafa.security import get_password_hash

fake = Faker()


def seed_users(session: Session):
    organizacoes = session.query(Organization).all()
    organizacao_ids = [org.id for org in organizacoes]

    if not organizacao_ids:
        return 'Não há organizações cadastradas!'

    for _ in range(10):  # Gera 10 usuários fictícios
        dados = {
            'primeiro_nome': fake.first_name(),
            'sobrenome': fake.last_name(),
            'email': fake.unique.email(),
            'username': fake.user_name(),
            'senha_hash': get_password_hash(fake.password()),
            'telefone': fake.phone_number()[:20],
            'eh_deleted': fake.boolean(chance_of_getting_true=5),
            'eh_voluntario': fake.boolean(chance_of_getting_true=50),
            'eh_gerente': fake.boolean(chance_of_getting_true=50),
            'id_organizacao': choice(organizacao_ids),
            'deficiencia_auditiva': None,
            'usa_cadeira_rodas': None,
            'deficiencia_cognitiva': None,
            'lgbtq': None,
            'url_imagem_perfil': None,
        }

        novo_usuario_data = User.CreateUser(**dados)
        novo_usuario = User.create(novo_usuario_data)
        db_usuario = session.scalar(
            select(User).where(User.email == novo_usuario.email)
        )

        if db_usuario is None:
            session.add(novo_usuario)
            session.commit()
            session.refresh(novo_usuario)
    return 'Usuários criados com sucesso!'


def undo_users(session):
    session.execute(text('DELETE FROM users;'))
    session.execute(text('DELETE FROM sqlite_sequence WHERE name="users";'))
    session.commit()
