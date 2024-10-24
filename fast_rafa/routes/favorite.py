import re
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_rafa.database import get_session
from fast_rafa.models.favorite import Favorite
from fast_rafa.models.post import Post
from fast_rafa.models.user import User

router = APIRouter()


@router.post(
    '/{id_usuario}/{id_postagem}',
    status_code=HTTPStatus.CREATED,
    response_model=Favorite,
)
def create_favorite(
    id_usuario: int,
    id_postagem: int,
    db: Session = Depends(get_session)
):
    usuario = db.query(User).filter(User.id == id_usuario).first()

    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado'
        )

    postagem = db.query(Post).filter(Post.id == id_postagem).first()

    if not postagem:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Postagem não encontrada'
        )

    favorito_existente = db.query(Favorite).filter_by(
        id_usuario=id_usuario, id_postagem=id_postagem
    ).first()

    if favorito_existente:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Este item já foi favoritado pelo usuário."
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
            r'UNIQUE constraint failed: users\.(\w+)', error_message)
        if match:
            field_name = match.group(1).replace('_', ' ').capitalize()
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=f"Já existe um favorito com este(a) {field_name}."
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Erro ao adicionar favorito."
            )

    return novo_favorito


@router.get('/{id_favorite}', status_code=HTTPStatus.OK)
def read_favorite_by_id(
    id_favorite: int,
    db: Session = Depends(get_session)
):
    favorito = db.query(Favorite).filter(
        Favorite.id == id_favorite
    ).first()

    if not favorito:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Favorito não encontrado'
        )

    return favorito


@router.get(
    '/usuario/{id_usuario}',
    status_code=HTTPStatus.OK
)
def read_favorites_by_user(
    id_usuario: int,
    db: Session = Depends(get_session)
):
    usuario = db.query(User).filter(User.id == id_usuario).first()

    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado'
        )

    favoritos = db.query(Favorite).filter(
        Favorite.id_usuario == id_usuario
    ).all()

    if not favoritos:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Nenhum favorito encontrado'
        )

    return favoritos


@router.get(
    '/postagem/{id_postagem}',
    status_code=HTTPStatus.OK
)
def read_favorites_by_post(
    id_postagem: int,
    db: Session = Depends(get_session)
):
    postagem = db.query(Post).filter(Post.id == id_postagem).first()

    if not postagem:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Postagem não encontrada'
        )

    favoritos = db.query(Favorite).filter(
        Favorite.id_postagem == id_postagem
    ).all()

    if not favoritos:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Nenhum favorito encontrado'
        )

    return favoritos


@router.delete(
    '/{id_favorite}',
    status_code=HTTPStatus.OK,
    response_model=User.DeleteResponse,
)
def delete_favorite(
    id_favorite: int,
    db: Session = Depends(get_session)
):
    favorito = db.query(Favorite).filter(Favorite.id == id_favorite).first()

    if not favorito:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Favorito não encontrado'
        )

    try:
        db.delete(favorito)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)

        if ('foreign key constraint' in error_message.lower() or
                'constraint failed' in error_message.lower()):
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=(
                    "Não é possível excluir o favorito, "
                    "pois está associado a outros registros."
                ),
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Erro ao excluir o favorito.",
            )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Erro inesperado ao excluir o favorito: {str(e)}"
        )

    return User.DeleteResponse(
        message="Favorito excluído com sucesso."
    )
