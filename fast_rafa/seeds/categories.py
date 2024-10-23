from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_rafa.database import get_session
from fast_rafa.models.category import Category


def seed_categories(session: Session = Depends(get_session)):
    laticinios = Category(
        categoria='Laticínios'
    )
    db_lat = session.scalar(
        select(Category).where(
            (Category.categoria == 'Laticínios')
        )
    )

    if db_lat is None:
        session.add(laticinios)
        session.commit()
        session.refresh(db_lat)

    vegetais = Category(
        categoria='Vegetais'
    )
    db_veg = session.scalar(
        select(Category).where(
            (Category.categoria == 'Vegetais')
        )
    )

    if db_veg is None:
        session.add(vegetais)
        session.commit()
        session.refresh(db_veg)

    frutas = Category(
        categoria='Frutas'
    )

    db_fru = session.scalar(
        select(Category).where(
            (Category.categoria == 'Frutas')
        )
    )

    if db_fru is None:
        session.add(frutas)
        session.commit()
        session.refresh(db_fru)

    graos = Category(
        categoria='Grãos'
    )

    db_gra = session.scalar(
        select(Category).where(
            (Category.categoria == 'Grãos')
        )
    )

    if db_gra is None:
        session.add(graos)
        session.commit()
        session.refresh(db_gra)

    proteinas = Category(
        categoria='Proteínas'
    )

    db_pro = session.scalar(
        select(Category).where(
            (Category.categoria == 'Proteínas')
        )
    )

    if db_pro is None:
        session.add(proteinas)
        session.commit()
        session.refresh(db_pro)


def undo_categories(session: Session = Depends(get_session)):
    session.execute('TRUNCATE categories RESTART IDENTITY CASCADE;')
    session.commit()
