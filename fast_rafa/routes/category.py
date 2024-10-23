from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from fast_rafa.database import get_session
from fast_rafa.models.category import Category

router = APIRouter()


@router.post('/', status_code=HTTPStatus.CREATED, response_model=Category)
def create_category(
    categoria: str,
    db: Session = Depends(get_session)
):

    categoria = categoria.strip()
    categoria_existe = (
        db.query(Category)
        .filter(
            func.upper(Category.categoria) == categoria.strip().upper()
        )
        .first()
    )

    if categoria_existe:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Uma categoria com este nome já existe.'
        )
    nova_categoria = Category.create(categoria=categoria)

    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)

    return nova_categoria


@router.get('/', status_code=HTTPStatus.OK)
def read_categories(
   db: Session = Depends(get_session)
):
    todas_categorias = db.scalars(select(Category)).all()

    if not todas_categorias:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Nenhuma categoria encontrada'
        )

    categorias_dics = [categoria.to_dict() for categoria in todas_categorias]
    return {'categorias': categorias_dics}


@router.get(
    '/{category_id}', status_code=HTTPStatus.OK
)
def read_category_by_id(category_id: int, db: Session = Depends(get_session)):
    categoria_db = db.scalar(
        select(Category).where(Category.id == category_id)
    )

    if not categoria_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Categoria não encontrada'
        )

    return categoria_db.to_dict()


@router.get('/name/{category_name}',
            status_code=HTTPStatus.OK,
            response_model=List[Category])
def read_category_by_name(
    category_name: str,
    db: Session = Depends(get_session)
):

    categoria_formatada = Category.read_by_name(category_name)

    categoria_db = db.scalars(
        select(Category).where(
            func.upper(Category.categoria).like(f'%{categoria_formatada}%')
        )
    ).all()

    if not categoria_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Categoria não encontrada'
        )

    return [categoria.to_dict() for categoria in categoria_db]


@router.put("/{category_id}",
            response_model=Category.UpdateResponse)
def update_category(
    category_id: int,
    category_data: Category.UpdateRequest,
    db: Session = Depends(get_session)
):
    categoria = db.query(Category).filter(Category.id == category_id).first()

    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    nome_categoria_original = categoria.categoria.strip()
    nome_categoria_novo = category_data.categoria.strip()

    if nome_categoria_original == nome_categoria_novo:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='O nome da categoria não pode ser o mesmo.'
        )

    categoria_existe = (
        db.query(Category)
        .filter(func.upper(Category.categoria) == nome_categoria_novo.upper())
        .first()
    )

    if categoria_existe:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Uma categoria com este nome já existe.'
        )

    updated_category = Category.update(categoria, category_data.categoria)

    db.add(updated_category)
    db.commit()
    db.refresh(updated_category)

    return Category.UpdateResponse(
        message=(
            f'A categoria "{nome_categoria_original}" foi atualizada para '
            f'"{nome_categoria_novo}".'
        )
    )


@router.delete('/{category_id}', response_model=Category.DeleteResponse)
def delete_category(category_id: int, db: Session = Depends(get_session)):
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Categoria não encontrada'
        )

    deleted_category = Category.delete(categoria=category.categoria)
    db.delete(category)
    db.commit()

    return Category.DeleteResponse(
        message=(
            f'A categoria "{deleted_category.categoria}" '
            'foi deletada com sucesso.'
        )
    )
