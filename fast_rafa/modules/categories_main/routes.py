import re
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_rafa.core.database import get_session
from fast_rafa.modules.categories_main.models import CategoryMain
from fast_rafa.modules.categories_main.schemas import (
    CategoryMainCreate,
    CategoryMainDeleteResponse,
    CategoryMainUpdateRequest,
    CategoryMainUpdateResponse,
)
from fast_rafa.utils.error_messages import (
    get_conflict_message,
    get_creation_error_message,
    get_deletion_error_message,
    get_not_found_message,
    get_success_message,
    get_unexpected_error_message,
    get_update_error_message,
)

router = APIRouter()


@router.post('/', status_code=HTTPStatus.CREATED, response_model=dict)
def create_category(
    categoria: CategoryMainCreate, db: Session = Depends(get_session)
):
    nova_categoria = CategoryMain.create(categoria)

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


@router.get('/', status_code=HTTPStatus.OK, response_model=list[CategoryMain])
def read_categories(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_session)
):
    todas_categorias = db.query(CategoryMain).offset(skip).limit(limit).all()

    if not todas_categorias:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Categoria'),
        )

    return todas_categorias


@router.get('/{category_id}', status_code=HTTPStatus.OK)
def read_category_by_id(category_id: int, db: Session = Depends(get_session)):
    categoria_db = (
        db.query(CategoryMain).filter(CategoryMain.id == category_id).first()
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
    response_model=List[CategoryMain],
)
def read_category_by_name(
    category_name: str, db: Session = Depends(get_session)
):
    categorias = (
        db.query(CategoryMain)
        .filter(CategoryMain.categoria.ilike(f'%{category_name}%'))
        .all()
    )

    if not categorias:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Categoria'),
        )

    return categorias


@router.put('/{category_id}', response_model=CategoryMainUpdateResponse)
def update_category(
    category_id: int,
    category_data: CategoryMainUpdateRequest,
    db: Session = Depends(get_session),
):
    categoria = (
        db.query(CategoryMain).filter(CategoryMain.id == category_id).first()
    )

    if categoria is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Categoria'),
        )

    # nome_categoria_original = categoria.categoria.strip()

    categoria_atualizada = CategoryMain.update(categoria, category_data.dict())

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

    return CategoryMainUpdateResponse(
        message=get_success_message('Categoria atualizada')
    )


@router.delete('/{category_id}', response_model=CategoryMainDeleteResponse)
def delete_category(category_id: int, db: Session = Depends(get_session)):
    category = (
        db.query(CategoryMain).filter(CategoryMain.id == category_id).first()
    )

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

        match = re.search(
            r'UNIQUE constraint failed: categories\.(\w+)', error_message
        )
        if match:
            field_name = match.group(1).replace('_', ' ').capitalize()
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=get_conflict_message(field_name),
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
            detail=get_unexpected_error_message('deletar a categoria', str(e)),
        )

    return CategoryMainDeleteResponse(
        message=get_success_message('Categoria excluída')
    )
