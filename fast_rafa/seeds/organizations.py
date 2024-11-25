from datetime import datetime

from faker import Faker
from sqlalchemy.exc import SQLAlchemyError

from fast_rafa.core.logger import setup_logger
from fast_rafa.modules.organizations.models import (
    Organization,
    OrganizationCreate,
)
from fast_rafa.utils.funcs import generate_unique_url

fake = Faker('pt_BR')
logger = setup_logger()


def gen_random_time():
    hour = fake.random_int(min=0, max=23)
    minute = fake.random_int(min=0, max=59)
    second = fake.random_int(min=0, max=59)
    return f'{hour:02}:{minute:02}:{second:02}'


async def seed_organizations(session):
    MAX_ORGANIZACOES = 10
    MAX_TENTATIVAS = 3
    organizacoes_criadas = 0
    erros_consecutivos = 0

    try:
        logger.info(f'Iniciando criação de {MAX_ORGANIZACOES} organizações...')

        while organizacoes_criadas < MAX_ORGANIZACOES:
            if erros_consecutivos >= MAX_TENTATIVAS:
                logger.error(
                    f'Número máximo de tentativas ({MAX_TENTATIVAS})'
                    ' atingido. Parando execução após criar '
                    f'{organizacoes_criadas} organizações.'
                )
                break

            try:
                url_logo = generate_unique_url(
                    session, Organization, is_logo=True
                )
                url_imagem = generate_unique_url(
                    session, Organization, is_logo=False
                )

                if not url_logo:
                    url_logo = generate_unique_url(
                        session, Organization, is_logo=True
                    )
                if not url_imagem:
                    url_imagem = generate_unique_url(
                        session, Organization, is_logo=False
                    )

                dados = {
                    'id_federal': str(fake.unique.random_number(digits=14)),
                    'nao_governamental': fake.boolean(
                        chance_of_getting_true=50
                    ),
                    'url_logo': url_logo,
                    'url_imagem': url_imagem,
                    'abertura': gen_random_time(),
                    'fechamento': gen_random_time(),
                    'intervalo': f'{gen_random_time()} - {gen_random_time()}',
                    'nome': fake.company(),
                    'descricao': fake.text(max_nb_chars=200),
                    'rua': fake.street_name(),
                    'cep': fake.postcode(),
                    'cidade': fake.city(),
                    'estado': fake.state(),
                    'telefone': fake.phone_number(),
                    'email': fake.unique.email(),
                    'criado_em': datetime.utcnow(),
                    'atualizado_em': datetime.utcnow(),
                }

                organizacao_data = OrganizationCreate(**dados)
                organizacao = Organization.create(organizacao_data)

                session.add(organizacao)
                session.commit()
                session.refresh(organizacao)
                organizacoes_criadas += 1
                erros_consecutivos = 0
                logger.info(
                    f'Organização criada com sucesso: {organizacao.nome}'
                )

            except SQLAlchemyError as e:
                session.rollback()
                erros_consecutivos += 1
                logger.error(f'Erro ao criar organização: {str(e)}')
            except Exception as e:
                session.rollback()
                erros_consecutivos += 1
                logger.error(f'Erro inesperado ao criar organização: {str(e)}')

        if organizacoes_criadas == MAX_ORGANIZACOES:
            return f'Todas as {MAX_ORGANIZACOES} '
            'organizações foram criadas com sucesso!'
        else:
            return f'Processo finalizado com {organizacoes_criadas}'
            'organizações criadas. Algumas organizações não puderam'
            'ser criadas devido a erros.'
    except Exception as e:
        logger.error(
            'Erro fatal durante o seed de organizações', exc_info=True
        )
        return f'Erro durante a criação das organizações: {str(e)}'


async def undo_organizations(session):
    session.query(Organization).delete()
    session.commit()
    return 'Organizações deletadas com sucesso!'
