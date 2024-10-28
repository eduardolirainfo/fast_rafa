import re
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import select
from fast_rafa.database import get_session
from fast_rafa.models.favorite import Favorite
from fast_rafa.models.organization import Organization
from fast_rafa.models.user import User

router = APIRouter()


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=dict
)
def create_user(usuario: User.CreateUser, db: Session = Depends(get_session)):
    organizacao = (
        db.query(Organization)
        .filter(Organization.id == usuario.id_organizacao)
        .all()
    )

    if not organizacao:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Organização não encontrada',
        )

    novo_usuario = User.create(usuario)
    try:
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)

        match = re.search(
            r'UNIQUE constraint failed: users\.(\w+)', error_message
        )
        if match:
            field_name = match.group(1).replace('_', ' ').capitalize()
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=f'Já existe um usuário com este(a) {field_name}.',
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail='Erro ao criar o usuário.',
            )

    return novo_usuario.profile_dict()


@router.get('/', status_code=HTTPStatus.OK, response_model=list[dict])
def read_users(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_session)
):
    usuarios = db.query(User).offset(skip).limit(limit).all()

    if not usuarios:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Nenhum usuário encontrado!',
        )
    return [usuario.profile_dict() for usuario in usuarios]


@router.get('/{user_id}', status_code=HTTPStatus.OK, response_model=dict)
def read_user_by_id(user_id: int, db: Session = Depends(get_session)):

    usuario = db.scalar(select(User).filter(User.id == user_id))

    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado!',
        )
    else:
        usuario.favoritos = (
            db.query(Favorite).filter(Favorite.id_usuario == usuario.id).all()
        )
    return usuario.home_dict()


@router.get(
    '/mail/{user_email}', status_code=HTTPStatus.OK, response_model=dict
)
def read_dict_by_email(user_email: str, db: Session = Depends(get_session)):
    usuario = db.scalar(select(User).filter(User.email == user_email))

    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado!',
        )
    else:
        usuario.favoritos = (
            db.query(Favorite).filter(Favorite.id_usuario == usuario.id).all()
        )
    return usuario.home_dict()


@router.get(
    '/organization/{id_organizacao}',
    status_code=HTTPStatus.OK,
    response_model=List[dict],
)
def read_user_by_id_organization(
    id_organizacao: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_session),
):
    usuarios = (
        db.query(User)
        .filter(User.id_organizacao == id_organizacao)
        .offset(skip)
        .limit(limit)
        .all()
    )

    if not usuarios:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuários não encontrados!',
        )

    return [usuario.home_dict() for usuario in usuarios]


@router.put(
    '/{user_id}', status_code=HTTPStatus.OK, response_model=User.UpdateResponse
)
def update_user(
    user_id: int,
    user_data: User.UpdateRequest,
    db: Session = Depends(get_session),
):
    organization = (
        db.scalar(select(Organization).filter(
            Organization.id == user_data.id_organizacao))
    )

    if not organization:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Organização não encontrada',
        )

    usuario = db.scalar(select(User).filter(User.id == user_id))

    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado!',
        )

    usuario = User.update(usuario, user_data.dict())

    try:
        db.commit()
        db.refresh(usuario)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)

        match = re.search(
            r'UNIQUE constraint failed: users\.(\w+)', error_message
        )
        if match:
            field_name = match.group(1).replace('_', ' ').capitalize()
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=f'Já existe um usuário com este(a) {field_name}.',
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail='Erro ao atualizar o usuário.',
            )

    return User.UpdateResponse(message='Usuário atualizado com sucesso.')


@router.delete(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=User.DeleteResponse,
)
def delete_user(user_id: int, db: Session = Depends(get_session)):
    usuario = db.scalar(select(User).filter(User.id == user_id))

    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado!',
        )

    try:
        db.delete(usuario)
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
                detail=(
                    'Não é possível excluir o usuário, '
                    'pois está associado a outros registros.'
                ),
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail='Erro ao excluir o usuário.',
            )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Erro inesperado ao excluir o usuário: {str(e)}',
        )

    return User.DeleteResponse(message='Usuário excluído com sucesso.')