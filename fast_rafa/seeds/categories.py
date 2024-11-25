from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from fast_rafa.core.logger import setup_logger
from fast_rafa.modules.categories.models import Category
from fast_rafa.modules.categories.schemas import CreateCategory
from fast_rafa.modules.categories_main.models import CategoryMain
from fast_rafa.modules.categories_main.schemas import CategoryMainCreate
from fast_rafa.utils.funcs import gerar_slug

logger = setup_logger()


# Função para criar uma subcategoria associada a uma categoria principal
async def criar_categoria_fixa(
    session, categoria: str, id_categoria_principal: Optional[int]
) -> Optional[Category]:
    """Cria uma subcategoria, mas não recria categorias principais."""
    if id_categoria_principal is None:
        logger.warning(
            f"A subcategoria '{categoria}' não tem id_categoria_principal, "
            'pulando inserção.'
        )
        return None  # Retorna None se não tiver id_categoria_principal

    try:
        # Verificando se a subcategoria já existe para evitar duplicidade
        db_categoria = session.scalar(
            select(Category).where(
                Category.categoria == categoria
                and Category.id_categoria_principal == id_categoria_principal
            )
        )

        if db_categoria is None:
            # Gerando slug e icon para a subcategoria
            slug = gerar_slug(categoria)
            icon = f'{slug}-icon.svg'

            # Criando a subcategoria associada ao id_categoria_principal
            categoria_data = CreateCategory(
                categoria=categoria,
                slug=slug,
                icon=icon,
                id_categoria_principal=id_categoria_principal,
            )
            nova_categoria = Category.create(categoria_data)
            session.add(nova_categoria)
            session.commit()
            session.refresh(nova_categoria)
            logger.info(
                f'Subcategoria criada: {nova_categoria.categoria} associada à '
                f'categoria principal {nova_categoria.id_categoria_principal}.'
            )
            return nova_categoria
        else:
            logger.warning(
                f'Subcategoria já existe: {db_categoria.categoria}'
                ' associada à '
                f'categoria principal {db_categoria.id_categoria_principal}.'
            )
            return None
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f'Erro ao criar subcategoria: {str(e)}')
        return None


# Função para criar subcategorias
async def criar_subcategorias(
    session, categoria: str, subcategorias: list
) -> None:
    """Cria subcategorias para uma categoria principal já existente."""
    # Buscando o id_categoria_principal na tabela CategoryMain
    # (não cria a categoria principal)
    categoria_principal = session.scalar(
        select(CategoryMain).where(CategoryMain.categoria == categoria)
    )

    if categoria_principal:
        id_categoria_principal = categoria_principal.id
        logger.info(
            f'Categoria principal {categoria} encontrada com id '
            f'{id_categoria_principal}.'
        )
    else:
        logger.warning(
            f"Categoria principal '{categoria}' "
            'não encontrada em CategoryMain.'
        )
        return

    # Criando as subcategorias associadas ao id_categoria_principal
    for subcategoria in subcategorias:
        await criar_categoria_fixa(
            session, subcategoria, id_categoria_principal
        )


# Função principal para rodar a seed de categorias
async def seed_categories(session):
    """Executa o seed para categorias principais e suas subcategorias."""
    categorias_principais = [
        'Alimentos Frescos',
        'Não Perecíveis',
        'Prontos para Consumo',
        'Bebidas',
    ]  # Exemplo de categorias principais
    subcategorias_dict = {
        'Alimentos Frescos': ['Laticínios', 'Vegetais', 'Frutas', 'Carnes'],
        'Não Perecíveis': ['Grãos', 'Enlatados', 'Cereais'],
        'Prontos para Consumo': ['Congelados', 'Snacks', 'Pratos Prontos'],
        'Bebidas': ['Refrigerantes', 'Sucos', 'Águas', 'Alcoólicas'],
    }

    criadas_main = 0
    criadas_sub = 0
    logger.info('Iniciando seed de categorias principais e subcategorias...')

    # Criando categorias principais e suas subcategorias
    for categoria in categorias_principais:
        # Verificando se a categoria principal existe na tabela CategoryMain
        categoria_principal = session.scalar(
            select(CategoryMain).where(CategoryMain.categoria == categoria)
        )

        if categoria_principal:
            id_categoria_principal = categoria_principal.id
            logger.info(
                f'Categoria principal {categoria} já existente, id: '
                f'{id_categoria_principal}.'
            )
        else:
            logger.info(f'Criando categoria principal {categoria}...')
            categoria_data = CategoryMainCreate(
                categoria=categoria,
                slug=gerar_slug(categoria),
                icon=f'{gerar_slug(categoria)}-icon.svg',
            )
            nova_categoria_principal = CategoryMain.create(categoria_data)
            session.add(nova_categoria_principal)
            session.commit()
            session.refresh(nova_categoria_principal)
            logger.info(
                f'Categoria principal {nova_categoria_principal.categoria} '
                'criada com sucesso.'
            )
            id_categoria_principal = nova_categoria_principal.id
            criadas_main += 1

        # Criando subcategorias
        subcategorias = subcategorias_dict.get(categoria, [])
        await criar_subcategorias(session, categoria, subcategorias)
        criadas_sub += len(subcategorias)

    logger.info(
        f'Seed concluído. {criadas_main} categorias principais e '
        f'{criadas_sub} subcategorias criadas.'
    )
    return f'{criadas_main} categorias principais e'
    f'{criadas_sub} subcategorias incluídas com sucesso!'


async def undo_categories(session):
    """Remove todas as categorias e subcategorias criadas durante o seed."""
    try:
        categorias = session.execute(select(Category)).scalars().all()
        for categoria in categorias:
            session.delete(categoria)
        session.commit()
        logger.info('categorias removidas com sucesso.')

    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f'Erro ao desfazer a seed de categorias: {str(e)}')

    return 'Categorias removidas com sucesso!'
