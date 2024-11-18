import re
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_rafa.core.database import get_session
from fast_rafa.modules.favorites.models import Favorite
from fast_rafa.modules.posts.models import Post
from fast_rafa.modules.users.models import User
from fast_rafa.utils.error_messages import (
    get_conflict_message,
    get_creation_error_message,
    get_deletion_error_message,
    get_not_found_message,
    get_success_message,
    get_unexpected_error_message,
)

router = APIRouter()


@router.post(
    '/{id_usuario}/{id_postagem}',
    status_code=HTTPStatus.CREATED,
    response_model=Favorite,
)
def create_favorite(
    id_usuario: int, id_postagem: int, db: Session = Depends(get_session)
):
    usuario = db.query(User).filter(User.id == id_usuario).first()
    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Usuário'),
        )

    postagem = db.query(Post).filter(Post.id == id_postagem).first()
    if not postagem:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Post'),
        )

    favorito_existente = (
        db.query(Favorite)
        .filter_by(id_usuario=id_usuario, id_postagem=id_postagem)
        .first()
    )
    if favorito_existente:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=get_conflict_message('favorito'),
        )

    novo_favorito = Favorite(id_usuario=id_usuario, id_postagem=id_postagem)
    try:
        db.add(novo_favorito)
        db.commit()
        db.refresh(novo_favorito)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)
        match = re.search(
            r'UNIQUE constraint failed: favorites\.(\w+)', error_message
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
                detail=get_creation_error_message('favorito'),
            )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=get_creation_error_message('favorito', str(e)),
        )

    return novo_favorito


@router.get('/{id_favorite}', status_code=HTTPStatus.OK)
def read_favorite_by_id(id_favorite: int, db: Session = Depends(get_session)):
    favorito = db.query(Favorite).filter(Favorite.id == id_favorite).first()
    if not favorito:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Favorito'),
        )

    return favorito


@router.get(
    '/user/{id_usuario}',
    status_code=HTTPStatus.OK,
    response_model=list[Favorite],
)
def read_favorites_by_user(
    id_usuario: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_session),
):
    usuario = db.query(User).filter(User.id == id_usuario).first()
    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Usuário'),
        )

    favoritos = (
        db.query(Favorite)
        .filter(Favorite.id_usuario == id_usuario)
        .offset(skip)
        .limit(limit)
        .all()
    )
    if not favoritos:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Favorito'),
        )

    return favoritos


@router.get('/post/{id_postagem}', status_code=HTTPStatus.OK)
def read_favorites_by_post(
    id_postagem: int, db: Session = Depends(get_session)
):
    postagem = db.query(Post).filter(Post.id == id_postagem).first()
    if not postagem:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Post'),
        )

    favoritos = (
        db.query(Favorite).filter(Favorite.id_postagem == id_postagem).all()
    )
    if not favoritos:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Favorito'),
        )

    return favoritos


@router.delete(
    '/{id_favorite}',
    status_code=HTTPStatus.OK,
    response_model=Favorite.DeleteResponseFavorite,
)
def delete_favorite(id_favorite: int, db: Session = Depends(get_session)):
    favorito = db.query(Favorite).filter(Favorite.id == id_favorite).first()
    if not favorito:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Favorito'),
        )

    try:
        db.delete(favorito)
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
                detail=get_deletion_error_message('favorito'),
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=get_deletion_error_message('favorito'),
            )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=get_unexpected_error_message('excluir favorito', str(e)),
        )

    return Favorite.DeleteResponseFavorite(
        message=get_success_message('Favorito excluído'),
    )
