from typing import Optional

from faker import Faker
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from fast_rafa.core.logger import setup_logger
from fast_rafa.modules.categories.models import Category
from fast_rafa.modules.categories.schemas import CreateCategory

fake = Faker('pt_BR')
logger = setup_logger()


async def criar_categoria_fixa(session, categoria: str) -> Optional[Category]:
    """Cria uma categoria fixa se ainda não existir."""
    try:
        categoria_data = CreateCategory(categoria=categoria)
        nova_categoria = Category.create(categoria_data)

        # Verifica se a categoria já existe
        db_categoria = session.scalar(
            select(Category).where(
                Category.categoria == nova_categoria.categoria
            )
        )

        if db_categoria is None:
            session.add(nova_categoria)
            session.commit()
            session.refresh(nova_categoria)
            logger.info(f'Categoria fixa criada: {nova_categoria.categoria}')
            return nova_categoria
        else:
            logger.warning(
                f'Categoria fixa já existe: {nova_categoria.categoria}'
            )
            return None
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f'Erro ao criar categoria fixa: {str(e)}')
        return None


async def criar_categoria_dinamica(session) -> Optional[Category]:
    """Cria uma categoria dinâmica usando dados gerados pelo Faker."""
    try:
        dados = {
            'categoria': fake.word().capitalize(),
        }

        categoria_data = CreateCategory(**dados)
        nova_categoria = Category.create(categoria_data)

        # Verifica se a categoria já existe
        db_categoria = session.scalar(
            select(Category).where(
                Category.categoria == nova_categoria.categoria
            )
        )

        if db_categoria is None:
            session.add(nova_categoria)
            session.commit()
            session.refresh(nova_categoria)
            logger.info(
                f'Categoria dinâmica criada: {nova_categoria.categoria}'
            )
            return nova_categoria
        else:
            logger.warning(
                f'Categoria dinâmica já existe: {nova_categoria.categoria}'
            )
            return None
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f'Erro ao criar categoria dinâmica: {str(e)}')
        return None


async def seed_categories(session):
    categorias_fixas = [
        'Laticínios',
        'Vegetais',
        'Frutas',
        'Grãos',
        'Proteínas',
    ]
    MAX_DINAMICAS = 10  # Número de categorias dinâmicas adicionais
    criadas_fixas = 0
    criadas_dinamicas = 0

    logger.info('Iniciando seed de categorias...')

    # Criando categorias fixas
    for categoria in categorias_fixas:
        if await criar_categoria_fixa(session, categoria):
            criadas_fixas += 1

    # Criando categorias dinâmicas
    while criadas_dinamicas < MAX_DINAMICAS:
        if await criar_categoria_dinamica(session):
            criadas_dinamicas += 1

    logger.info(
        f'Seed de categorias concluído. {criadas_fixas}'
        'fixas e {criadas_dinamicas} dinâmicas criadas.'
    )
    return f'{criadas_fixas} categorias fixas e '
    f'{criadas_dinamicas} dinâmicas incluídas com sucesso!'


async def undo_categories(session):
    # Deleta todos os registros da tabela 'categories'
    session.query(Category).delete()
    session.commit()
    logger.info('Categorias removidas com sucesso!')
    return 'Categorias removidas com sucesso!'
