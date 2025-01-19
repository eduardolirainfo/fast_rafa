from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from fast_rafa.core.logger import setup_logger
from fast_rafa.modules.categories_main.models import CategoryMain
from fast_rafa.modules.categories_main.schemas import CategoryMainCreate
from fast_rafa.utils.funcs import gerar_slug

logger = setup_logger()


async def criar_categoria_main_fixa(
    session, categoria: str, icon: str
) -> Optional[CategoryMain]:
    """Cria uma categoria principal fixa se ainda não existir."""
    try:
        slug = gerar_slug(categoria)
        categoria_data = CategoryMainCreate(
            categoria=categoria, slug=slug, icon=icon
        )
        nova_categoria_main = CategoryMain.create(categoria_data)

        # Verifica se a categoria principal já existe
        db_categoria_main = session.scalar(
            select(CategoryMain).where(
                CategoryMain.categoria == nova_categoria_main.categoria
            )
        )

        if db_categoria_main is None:
            session.add(nova_categoria_main)
            session.commit()
            session.refresh(nova_categoria_main)
            logger.info(
                'Categoria principal fixa criada: '
                f'{nova_categoria_main.categoria}'
            )
            return nova_categoria_main
        else:
            logger.warning(
                'Categoria principal fixa já existe: '
                f'{nova_categoria_main.categoria}'
            )
            return db_categoria_main
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f'Erro ao criar categoria principal fixa: {str(e)}')
        return None


async def seed_categories_main(session):
    categorias_main_fixas = [
        {'categoria': 'Alimentos Frescos', 'icon': 'fresh-food-icon.svg'},
        {'categoria': 'Não Perecíveis', 'icon': 'non-perishable-icon.svg'},
        {'categoria': 'Prontos para Consumo', 'icon': 'ready-to-eat-icon.svg'},
        {'categoria': 'Bebidas', 'icon': 'beverages-icon.svg'},
    ]
    criadas_main = 0

    logger.info('Iniciando seed de categorias principais...')

    # Criando categorias principais fixas
    for categoria_main in categorias_main_fixas:
        if await criar_categoria_main_fixa(
            session, categoria_main['categoria'], categoria_main['icon']
        ):
            criadas_main += 1

    logger.info(
        f'Seed de categorias principais concluído. {criadas_main} criadas.'
    )
    return f'{criadas_main} categorias principais incluídas com sucesso!'


async def undo_categories_main(session):
    # Deleta todos os registros da tabela 'categories_main'
    session.query(CategoryMain).delete()
    session.commit()
    logger.info('Categorias principais removidas com sucesso!')
    return 'Categorias principais removidas com sucesso!'
