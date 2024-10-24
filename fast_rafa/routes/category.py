
import re
from http import HTTPStatus
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_rafa.database import get_session
from fast_rafa.models.category import Category

router = APIRouter()


@router.post('/', status_code=HTTPStatus.CREATED, response_model=Category)
def create_category(
    categoria: Category.Create,
    db: Session = Depends(get_session)
):
    nova_categoria = Category.create(categoria)

    try:
        db.add(nova_categoria)
        db.commit()
        db.refresh(nova_categoria)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)

        match = re.search(
            r'UNIQUE constraint failed: categories\.categoria', error_message
        )
        if match:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Essa categoria já existe."
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Erro ao criar a categoria."
            )

    return nova_categoria


@router.get('/', status_code=HTTPStatus.OK)
def read_categories(
   db: Session = Depends(get_session)
):
    todas_categorias = db.query(Category).all()

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
    categoria_db = db.query(Category).filter(
        Category.id == category_id).first()

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
    categorias = db.query(Category).filter(
        Category.categoria.ilike(f'%{category_name}%')
    ).all()

    if not categorias:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Nenhuma categoria encontrada'
        )

    return categorias


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
    # nome_categoria_novo = category_data.categoria.strip()

    # if nome_categoria_original == nome_categoria_novo:
    #     raise HTTPException(
    #         status_code=HTTPStatus.BAD_REQUEST,
    #         detail="O nome da categoria não pode ser o mesmo."
    #     )

    categoria_atualizada = Category.update(categoria, category_data.dict())

    try:
        db.commit()
        db.refresh(categoria_atualizada)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)

        match = re.search(
            r'UNIQUE constraint failed: categories\.categoria', error_message
        )
        if match:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Essa categoria já existe."
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Erro ao criar a categoria."
            )

    return Category.UpdateResponse(
        message=(
            f'A categoria "{nome_categoria_original}" foi atualizada para '
            f'"{categoria_atualizada.categoria}".'
        )
    )


@router.delete('/{category_id}',
               response_model=Category.DeleteResponse)
def delete_category(
    category_id: int,
    db: Session = Depends(get_session)
):
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Categoria não encontrada'
        )

    try:
        db.delete(category)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)

        if ('foreign key constraint' in error_message.lower() or
                'constraint failed' in error_message.lower()):
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=(
                    "Não é possível excluir essa categoria, "
                    "pois ela está associada a uma postagem."
                ),
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail='Erro ao deletar a categoria.'
            )
    return Category.DeleteResponse(
        message=(
            f'A categoria "{category.categoria}" '
            'foi deletada com sucesso.'
        )
    )
