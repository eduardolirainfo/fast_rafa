import re
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_rafa.database import get_session
from fast_rafa.messages.error_messages import (
    get_conflict_message,
    get_creation_error_message,
    get_not_found_message,
    get_success_message,
    get_unexpected_error_message,
    get_update_error_message,
)
from fast_rafa.models.delivery import Delivery
from fast_rafa.models.event import Event
from fast_rafa.models.favorite import Favorite
from fast_rafa.models.message import Message
from fast_rafa.models.organization import Organization
from fast_rafa.models.post import Post
from fast_rafa.models.user import User
from fast_rafa.models.watchlist import Watchlist
from fast_rafa.schemas.user import (
    CreateUser,
    CreateUserResponse,
    DeleteUserResponse,
    UpdateUserRequest,
    UpdateUserResponse,
    UserResponse,
)
from fast_rafa.security import (
    get_current_user,
    get_password_hash,
)
from fast_rafa.utils.sel import get_by_sel

router = APIRouter()


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=CreateUserResponse
)
def create_user(usuario: CreateUser, db: Session = Depends(get_session)):
    organizacao = (
        db.query(Organization)
        .filter(Organization.id == usuario.id_organizacao)
        .all()
    )

    if not organizacao:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=get_not_found_message('Organização'),
        )

    senha_hash = get_password_hash(usuario.senha_hash)
    novo_usuario_data = usuario.dict()
    novo_usuario_data['senha_hash'] = senha_hash
    novo_usuario = User.create(CreateUser(**novo_usuario_data))
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
                detail=get_conflict_message(field_name),
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=get_creation_error_message('usuário'),
            )

    return CreateUserResponse(message=get_success_message('Usuário criado'))


@router.get(
    '/home', status_code=HTTPStatus.OK, response_model=list[UserResponse]
)
def read_users_home(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    usuarios = (
        get_by_sel(db, User, current_user.id).offset(skip).limit(limit).all()
    )

    if not usuarios:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Nenhum usuário'),
        )

    users = [UserResponse.from_home(usuario) for usuario in usuarios]
    return users


@router.get(
    '/profile', status_code=HTTPStatus.OK, response_model=list[UserResponse]
)
def read_users_profile(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    usuarios = (
        get_by_sel(db, User, current_user.id).offset(skip).limit(limit).all()
    )

    if not usuarios:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Nenhum usuário'),
        )

    users = [UserResponse.from_profile(usuario) for usuario in usuarios]
    return users


@router.get('/full', status_code=HTTPStatus.OK, response_model=dict)
def read_users_full(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    usuarios = (
        get_by_sel(db, User, current_user.id).offset(skip).limit(limit).all()
    )

    if not usuarios:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Nenhum usuário'),
        )

    users = [UserResponse.from_home(usuario) for usuario in usuarios]
    return {'users': users}


@router.get(
    '/{user_id}', status_code=HTTPStatus.OK, response_model=UserResponse
)
def read_user_by_id(
    user_id: int,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    usuario = get_by_sel(
        db, User, current_user.id, filter_plus={'id': user_id}
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Usuário'),
        )
    else:
        usuario.favoritos = (
            db.query(Favorite).filter(Favorite.id_usuario == usuario.id).all()
        )

    user_by_id = UserResponse.from_home(usuario)
    return user_by_id


@router.get(
    '/mail/{user_email}',
    status_code=HTTPStatus.OK,
    response_model=UserResponse,
)
def read_user_by_email(
    user_email: str,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    usuario = get_by_sel(
        db, User, current_user.id, filter_plus={'email': user_email}
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Usuário'),
        )
    else:
        usuario.favoritos = (
            db.query(Favorite).filter(Favorite.id_usuario == usuario.id).all()
        )

    return usuario


@router.get(
    '/organization/{id_organizacao}',
    status_code=HTTPStatus.OK,
    response_model=dict,
)
def read_user_by_id_organization(
    id_organizacao: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    usuarios = (
        get_by_sel(
            db,
            User,
            current_user.id,
            filter_plus={'id_organizacao': id_organizacao},
        )
        .offset(skip)
        .limit(limit)
        .all()
    )

    if not usuarios:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Usuário'),
        )

    user_by_id_organization = [
        UserResponse.from_home(usuario) for usuario in usuarios
    ]

    return {'users': user_by_id_organization}


@router.put(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UpdateUserResponse,
)
def update_user(
    user_id: int,
    user_data: UpdateUserRequest,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    organization = get_by_sel(
        db,
        Organization,
        current_user.id,
        filter_plus={'id': user_data.id_organizacao},
    ).first()

    if not organization:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=get_not_found_message('Organização'),
        )

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Você não tem permissão para atualizar este usuário',
        )

    update_data = user_data.dict()

    if 'senha_hash' in update_data and update_data['senha_hash']:
        update_data['senha_hash'] = get_password_hash(
            update_data.pop('senha_hash')
        )

    usuario = User.update(current_user, update_data)

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
                detail=get_conflict_message(field_name),
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=get_update_error_message('usuário'),
            )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=get_unexpected_error_message('atualizar o usuário', str(e)),
        )

    return UpdateUserResponse(
        message=get_success_message('Usuário atualizado'),
    )


@router.delete(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=DeleteUserResponse,
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Você não tem permissão para atualizar este usuário',
        )

    if current_user.eh_deletado:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Este usuário já foi excluído',
        )

    tem_vinculos_impeditivos = (
        db.query(User)
        .filter(User.id == user_id)
        .outerjoin(Favorite, Favorite.id_usuario == User.id)
        .outerjoin(Post, Post.id_usuario == User.id)
        .outerjoin(Delivery, Delivery.id_usuario == User.id)
        .outerjoin(Event, Event.id_usuario == User.id)
        .outerjoin(Watchlist, Watchlist.id_usuario == User.id)
        .outerjoin(Message, Message.id_remetente == User.id)
        .filter(
            or_(
                Favorite.id.isnot(None),
                Post.id.isnot(None),
                Delivery.id.isnot(None),
                Event.id.isnot(None),
                Watchlist.id.isnot(None),
                Message.id.isnot(None),
            )
        )
        .first()
    ) is not None

    try:
        if tem_vinculos_impeditivos:
            current_user.eh_deletado = True
            db.add(current_user)
        else:
            db.delete(current_user)

        db.commit()

        if tem_vinculos_impeditivos:
            db.refresh(current_user)

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
                detail=get_conflict_message(field_name),
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=get_update_error_message('usuário'),
            )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=get_unexpected_error_message('deletar o usuário', str(e)),
        )

    mensagem = (
        'Usuário excluído permanentemente'
        if not tem_vinculos_impeditivos
        else 'Usuário desativado'
    )
    return DeleteUserResponse(message=get_success_message(mensagem))
