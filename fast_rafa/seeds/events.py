from datetime import datetime, timedelta
from random import choice
from typing import Optional

from faker import Faker
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from fast_rafa.core.logger import setup_logger  # Importando o setup_logger
from fast_rafa.modules.events.models import Event
from fast_rafa.modules.events.schemas import EventCreate
from fast_rafa.modules.organizations.models import Organization
from fast_rafa.modules.users.models import User
from fast_rafa.utils.funcs import gerar_slug

fake = Faker('pt_BR')
logger = setup_logger()  # Inicializando o logger


async def get_organizacoes_e_usuarios(session) -> tuple[list, list]:
    try:
        # Debug para verificar a query
        logger.debug('Executando queries para buscar organizações e usuários')

        organizacoes_result = session.execute(select(Organization.id))
        usuarios_result = session.execute(select(User.id))

        organizacoes = organizacoes_result.scalars().all()
        usuarios = usuarios_result.scalars().all()

        # Debug dos resultados
        logger.debug(f'Organizações encontradas: {len(organizacoes)}')
        logger.debug(f'Usuários encontrados: {len(usuarios)}')

        return organizacoes, usuarios
    except Exception as e:
        logger.error(
            f'Erro ao buscar organizações e usuários: {str(e)}', exc_info=True
        )
        return [], []


async def criar_evento(
    session, organizacoes: list, usuarios: list
) -> Optional[Event]:
    """Tenta criar um único evento"""
    try:
        dados = {
            'id_organizacao': choice(organizacoes),
            'id_usuario': choice(usuarios),
            'fechado': datetime.utcnow()
            + timedelta(days=fake.random_int(1, 10)),
            'titulo': fake.sentence(nb_words=4),
            'slug': gerar_slug(fake.sentence(nb_words=4)),
            'descricao': fake.text(max_nb_chars=200),
            'data': datetime.utcnow()
            + timedelta(days=fake.random_int(10, 30)),
            'url_imagem': fake.image_url(),
            'criado_em': datetime.utcnow(),
            'atualizado_em': datetime.utcnow(),
        }

        novo_evento_data = EventCreate(**dados)
        novo_evento = Event.create(novo_evento_data)

        # Verifica se o evento já existe
        db_evento = session.scalar(
            select(Event).where(Event.titulo == novo_evento.titulo)
        )

        if db_evento is None:
            session.add(novo_evento)
            session.commit()
            session.refresh(novo_evento)
            logger.info(f'Evento criado com sucesso: {novo_evento.titulo}')
            return novo_evento
        else:
            logger.warning(f'Evento já existe: {novo_evento.titulo}')
            return None

    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f'Erro ao criar evento: {str(e)}')
        return None
    except Exception as e:
        session.rollback()
        logger.error(f'Erro inesperado ao criar evento: {str(e)}')
        return None


async def seed_events(session):
    MAX_EVENTOS = 10
    MAX_TENTATIVAS = 3
    eventos_criados = 0
    erros_consecutivos = 0

    try:
        # Debug para verificar a sessão
        logger.debug(f'Tipo da sessão: {type(session)}')

        organizacoes, usuarios = await get_organizacoes_e_usuarios(session)

        # Debug para verificar os dados retornados
        logger.debug(f'Organizações: {organizacoes}')
        logger.debug(f'Usuários: {usuarios}')

        if not organizacoes or not usuarios:
            logger.warning('Não há organizações ou usuários cadastrados!')
            return 'Não há organizações ou usuários cadastrados!'

        logger.info(f'Iniciando criação de {MAX_EVENTOS} eventos...')

        while eventos_criados < MAX_EVENTOS:
            if erros_consecutivos >= MAX_TENTATIVAS:
                logger.error(
                    'Número máximo de tentativas'
                    f'({MAX_TENTATIVAS}) atingido.'
                    f'Parando execução após criar {eventos_criados} eventos.'
                )
                break

            try:
                evento = await criar_evento(session, organizacoes, usuarios)

                if evento:
                    eventos_criados += 1
                    erros_consecutivos = 0
                    logger.info(
                        f'Progresso:'
                        f'{eventos_criados}/{MAX_EVENTOS} eventos criados'
                    )
                else:
                    erros_consecutivos += 1
                    logger.warning(
                        'Tentativa falhou.'
                        f'Erros consecutivos: {erros_consecutivos}'
                    )
            except Exception as e:
                erros_consecutivos += 1
                logger.error(
                    f'Erro ao criar evento: {str(e)}\nStack trace:',
                    exc_info=True,
                )

                if erros_consecutivos >= MAX_TENTATIVAS:
                    break

        if eventos_criados == MAX_EVENTOS:
            return f'Todos os {MAX_EVENTOS} eventos foram criados com sucesso!'
        else:
            return (
                f'Processo finalizado com {eventos_criados} eventos criados. '
                f'Alguns eventos não puderam ser criados devido a erros.'
            )

    except Exception as e:
        logger.error('Erro fatal durante o seed de eventos', exc_info=True)
        return f'Erro durante a criação dos eventos: {str(e)}'


async def undo_events(session):
    try:
        session.query(Event).delete()
        session.commit()
        return 'Eventos deletados com sucesso!'
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f'Erro ao desfazer a seed de eventos: {str(e)}')
        return f'Erro ao desfazer a seed de eventos: {str(e)}'
