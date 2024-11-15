from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_rafa.database import get_session
from fast_rafa.models.category import Category
from fast_rafa.models.seed import SeedStatus


def seed_all(session: Session = Depends(get_session)):
    """Envie todos os dados iniciais apenas uma vez."""
    # Verifica se já foi executado
    seed_status = session.scalar(select(SeedStatus).where(SeedStatus.id == 1))

    if seed_status is None:
        # Adiciona um novo status de seed
        session.add(SeedStatus(id=1, seeded=True))
        session.commit()

        # Chama a função para seed das categorias
        seed_categories(session)
        print('Inclusão de dados iniciais realizada com sucesso!')
    else:
        print('Os dados iniciais já foram inseridos.')


def seed_categories(session: Session = Depends(get_session)):
    categorias = [
        {'categoria': 'Laticínios'},
        {'categoria': 'Vegetais'},
        {'categoria': 'Frutas'},
        {'categoria': 'Grãos'},
        {'categoria': 'Proteínas'},
    ]

    for cat in categorias:
        nova_categoria_data = Category.CreateCategory(**cat)

        nova_categoria = Category.create(nova_categoria_data)

        db_categoria = session.scalar(
            select(Category).where(
                Category.categoria == nova_categoria.categoria
            )
        )

        if db_categoria is None:
            session.add(nova_categoria)
            session.commit()
            session.refresh(nova_categoria)

    return 'Categorias incluídas com sucesso!'


def undo_categories(session: Session = Depends(get_session)):
    session.execute('TRUNCATE categories RESTART IDENTITY CASCADE;')
    session.commit()
