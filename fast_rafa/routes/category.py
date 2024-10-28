import re
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_rafa.database import get_session
from fast_rafa.messages.error_messages import (
    get_conflict_message,
    get_creation_error_message,
    get_deletion_error_message,
    get_not_found_message,
    get_success_message,
    get_unexpected_error_message,
    get_update_error_message,
)
from fast_rafa.models.category import Category

router = APIRouter()


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=dict)
def create_category(
    categoria: Category.CreateCategory,
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
            r'UNIQUE constraint failed: categories\.(\w+)', error_message
        )
        if match:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=get_conflict_message('categoria'),
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=get_creation_error_message('categoria'),
            )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=get_unexpected_error_message('criar a categoria', str(e)),
        )

    return nova_categoria.to_dict()


@router.get('/', status_code=HTTPStatus.OK, response_model=list[Category])
def read_categories(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_session)
):
    todas_categorias = db.query(Category).offset(skip).limit(limit).all()

    if not todas_categorias:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Categoria'),
        )

    return todas_categorias


@router.get('/{category_id}', status_code=HTTPStatus.OK)
def read_category_by_id(category_id: int, db: Session = Depends(get_session)):
    categoria_db = (
        db.query(Category).filter(Category.id == category_id).first()
    )

    if not categoria_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Categoria'),
        )

    return categoria_db.to_dict()


@router.get(
    '/name/{category_name}',
    status_code=HTTPStatus.OK,
    response_model=List[Category],
)
def read_category_by_name(
    category_name: str, db: Session = Depends(get_session)
):
    categorias = (
        db.query(Category)
        .filter(Category.categoria.ilike(f'%{category_name}%'))
        .all()
    )

    if not categorias:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Categoria'),
        )

    return categorias


@router.put('/{category_id}', response_model=Category.UpdateResponse)
def update_category(
    category_id: int,
    category_data: Category.UpdateRequest,
    db: Session = Depends(get_session),
):
    categoria = db.query(Category).filter(Category.id == category_id).first()

    if categoria is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Categoria'),
        )

    # nome_categoria_original = categoria.categoria.strip()

    categoria_atualizada = Category.update(categoria, category_data.dict())

    try:
        db.commit()
        db.refresh(categoria_atualizada)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)

        match = re.search(
            r'UNIQUE constraint failed: categories\.(\w+)', error_message
        )
        if match:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=get_conflict_message('categoria'),
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=get_update_error_message('categoria'),
            )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=get_unexpected_error_message(
                'atualizar a categoria', str(e)
            ),
        )

    return Category.UpdateResponse(
        message=get_success_message('Categoria atualizada')
    )


@router.delete('/{category_id}', response_model=Category.DeleteResponse)
def delete_category(category_id: int, db: Session = Depends(get_session)):
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Categoria não encontrada'),
        )

    try:
        db.delete(category)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)

        if (
            'foreign key constraint' in error_message.lower()
            or 'constraint failed' in error_message.lower()
        ):
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=get_conflict_message('categoria'),
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=get_deletion_error_message('categoria'),
            )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=get_unexpected_error_message('excluir a categoria', str(e)),
        )

    return Category.DeleteResponse(
        message=get_success_message('Categoria excluída')
    )
