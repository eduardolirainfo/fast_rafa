from random import choice
from typing import Optional

from faker import Faker
from sqlalchemy import select

from fast_rafa.core.logger import setup_logger
from fast_rafa.core.security import get_password_hash
from fast_rafa.modules.organizations.models import Organization
from fast_rafa.modules.users.models import User
from fast_rafa.modules.users.schemas import CreateUser

fake = Faker('pt_BR')
logger = setup_logger()


async def get_organizacoes(session) -> list:
    """Busca organizações na base de dados"""
    try:
        logger.debug('Executando query para buscar organizações')
        organizacoes_result = session.execute(select(Organization.id))
        organizacoes = organizacoes_result.scalars().all()

        logger.debug(f'Organizações encontradas: {len(organizacoes)}')
        return organizacoes
    except Exception as e:
        logger.error(f'Erro ao buscar organizações: {str(e)}', exc_info=True)
        return []


async def criar_usuario(session, organizacoes: list) -> Optional[User]:
    """Tenta criar um único usuário"""
    try:
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
            'id_organizacao': choice(organizacoes),
            'deficiencia_auditiva': None,
            'usa_cadeira_rodas': None,
            'deficiencia_cognitiva': None,
            'lgbtq': None,
            'url_imagem_perfil': None,
        }

        novo_usuario_data = CreateUser(**dados)
        novo_usuario = User.create(novo_usuario_data)

        # Verifica se o usuário já existe
        db_usuario = session.scalar(
            select(User).where(User.email == novo_usuario.email)
        )

        if db_usuario is None:
            session.add(novo_usuario)
            session.commit()
            session.refresh(novo_usuario)
            logger.info(f'Usuário criado com sucesso: {novo_usuario.email}')
            return novo_usuario
        else:
            logger.warning(f'Usuário já existe: {novo_usuario.email}')
            return None

    except Exception as e:
        session.rollback()
        logger.error(f'Erro ao criar usuário: {str(e)}', exc_info=True)
        return None


async def seed_users(session):
    MAX_USUARIOS = 10
    MAX_TENTATIVAS = 3
    usuarios_criados = 0
    erros_consecutivos = 0

    try:
        # Busca as organizações
        organizacoes = await get_organizacoes(session)

        if not organizacoes:
            logger.warning('Não há organizações cadastradas!')
            return 'Não há organizações cadastradas!'

        logger.info(f'Iniciando criação de {MAX_USUARIOS} usuários...')

        while usuarios_criados < MAX_USUARIOS:
            if erros_consecutivos >= MAX_TENTATIVAS:
                logger.error(
                    f'Número máximo de tentativas ({MAX_TENTATIVAS})'
                    'atingido. Parando execução após criar '
                    f'{usuarios_criados} usuários.'
                )
                break

            try:
                usuario = await criar_usuario(session, organizacoes)

                if usuario:
                    usuarios_criados += 1
                    erros_consecutivos = 0
                    logger.info(
                        f'Progresso: {usuarios_criados}/{MAX_USUARIOS}'
                        'usuários criados'
                    )
                else:
                    erros_consecutivos += 1
                    logger.warning(
                        'Tentativa falhou. Erros consecutivos:'
                        f'{erros_consecutivos}'
                    )
            except Exception as e:
                erros_consecutivos += 1
                logger.error(f'Erro ao criar usuário: {str(e)}', exc_info=True)

                if erros_consecutivos >= MAX_TENTATIVAS:
                    break

        if usuarios_criados == MAX_USUARIOS:
            return (
                f'Todos os {MAX_USUARIOS} usuários foram criados com sucesso!'
            )
        else:
            return (
                f'Processo finalizado com {usuarios_criados}'
                'usuários criados. '
                f'Alguns usuários não puderam ser criados devido a erros.'
            )

    except Exception as e:
        logger.error('Erro fatal durante o seed de usuários', exc_info=True)
        return f'Erro durante a criação dos usuários: {str(e)}'


async def undo_users(session):
    result = session.query(User).delete()

    if result:
        session.commit()
        logger.info('Usuários excluídos com sucesso!')
        return 'Usuários excluídos com sucesso!'
    else:
        session.rollback()
        logger.error('Erro ao excluir usuários!')
        return 'Erro ao excluir usuários!'
