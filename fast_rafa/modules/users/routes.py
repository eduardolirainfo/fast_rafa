import re
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_rafa.core.database import get_session
from fast_rafa.core.security import (
    get_current_user,
    get_password_hash,
)
from fast_rafa.modules.deliveries.models import Delivery
from fast_rafa.modules.events.models import Event
from fast_rafa.modules.favorites.models import Favorite
from fast_rafa.modules.messages.models import Message
from fast_rafa.modules.organizations.models import Organization
from fast_rafa.modules.posts.models import Post
from fast_rafa.modules.users.models import User
from fast_rafa.modules.users.schemas import (
    CreateUser,
    DeleteUserResponse,
    UpdateUserRequest,
    UpdateUserResponse,
    UserResponse,
)
from fast_rafa.modules.watchlists.models import Watchlist
from fast_rafa.utils.error_messages import (
    get_conflict_message,
    get_creation_error_message,
    get_not_found_message,
    get_success_message,
    get_unexpected_error_message,
    get_update_error_message,
)
from fast_rafa.utils.sel import check_related_models, get_by_sel

router = APIRouter()


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserResponse)
def create_user(usuario: CreateUser, db: Session = Depends(get_session)):
    organizacao = get_by_sel(
        db,
        Organization,
        filters={
            'filter_plus': {'id': usuario.id_organizacao},
        },
    ).first()

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

    return UserResponse.from_home(novo_usuario)


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
        get_by_sel(db, User, current_user.id, filters={})
        .offset(skip)
        .limit(limit)
        .all()
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
        get_by_sel(db, User, current_user.id, filters={})
        .offset(skip)
        .limit(limit)
        .all()
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
        get_by_sel(db, User, current_user.id, filters={})
        .offset(skip)
        .limit(limit)
        .all()
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
        db, User, current_user.id, filters={'filter_plus': {'id': user_id}}
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
        db,
        User,
        current_user.id,
        filters={'filter_plus': {'email': user_email}},
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
            filters={
                'filter_plus': {'id_organizacao': id_organizacao},
            },
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


@router.patch('/{user_id}/status', status_code=HTTPStatus.OK)
def update_status(
    user_id: int,
    status: bool,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Você não tem permissão para atualizar este usuário',
        )

    if status:
        if current_user.eh_deletado:
            current_user.eh_deletado = False
        else:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Este usuário já está ativo',
            )
    elif not status:
        if not current_user.eh_deletado:
            current_user.eh_deletado = True
        else:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Este usuário já está inativo',
            )
    else:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Status inválido',
        )

    try:
        db.commit()
        db.refresh(current_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=get_unexpected_error_message(
                'atualizar o status do usuário', str(e)
            ),
        )

    return current_user


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
        filters={'filter_plus': {'id': user_data.id_organizacao}},
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

    return UpdateUserResponse.from_home(usuario)


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

    related_models = [Favorite, Post, Delivery, Event, Watchlist, Message]
    tem_vinculos_impeditivos = check_related_models(
        db=db,
        model=User,
        model_id=user_id,
        current_user_id=current_user.id,
        related_models=related_models,
    )

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
