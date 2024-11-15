import re
from http import HTTPStatus

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
from fast_rafa.models.organization import Organization
from fast_rafa.models.post import Post
from fast_rafa.models.user import User
from fast_rafa.schemas.post import (
    CreatePost,
    DeletePostResponse,
    PostRead,
    UpdatePostRequest,
    UpdatePostResponse,
)

router = APIRouter()


@router.post('/', status_code=HTTPStatus.CREATED, response_model=dict)
def create_post(post: CreatePost, db: Session = Depends(get_session)):
    categoria = (
        db.query(Category).filter(Category.id == post.id_categoria).all()
    )

    if not categoria:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=get_not_found_message('Categoria'),
        )

    organizacao = (
        db.query(Organization)
        .filter(Organization.id == post.id_organizacao)
        .all()
    )

    if not organizacao:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=get_not_found_message('Organização'),
        )

    usuario = db.query(User).filter(User.id == post.id_usuario).all()

    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=get_not_found_message('Usuário'),
        )
    nova_postagem = Post.create(post)

    try:
        db.add(nova_postagem)
        db.commit()
        db.refresh(nova_postagem)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)

        match = re.search(
            r'UNIQUE constraint failed: posts\.(\w+)', error_message
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
                detail=get_creation_error_message('post'),
            )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=get_unexpected_error_message('criar a postagem', str(e)),
        )
    novo_post = PostRead.from_orm(nova_postagem).to_dict()
    return novo_post


@router.get('/', status_code=HTTPStatus.OK, response_model=dict)
def read_posts(
    skip: int = 0,
    limit: int = 10,
    order_by: str = 'titulo',
    db: Session = Depends(get_session),
):
    postagens = (
        db.query(Post).order_by(order_by).offset(skip).limit(limit).all()
    )

    if not postagens:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Postagem'),
        )

    postagens = [PostRead.from_orm(post).to_dict() for post in postagens]

    return {'posts': postagens}


@router.get('/{post_id}', status_code=HTTPStatus.OK, response_model=dict)
def read_post_by_id(post_id: int, db: Session = Depends(get_session)):
    postagem = db.query(Post).filter(Post.id == post_id).first()

    if not postagem:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Postagem'),
        )
    post = PostRead.from_orm(postagem).to_dict()
    return post


@router.get(
    '/name/{post_name}', status_code=HTTPStatus.OK, response_model=dict
)
def read_post_by_name(post_name: str, db: Session = Depends(get_session)):
    postagens = (
        db.query(Post)
        .join(Category)
        .filter(
            (Post.titulo.ilike(f'%{post_name}%'))
            | (Post.descricao.ilike(f'%{post_name}%'))
        )
        .all()
    )

    if not postagens:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Postagem'),
        )

    post_by_name = [
        PostRead.from_orm(postagens).to_dict() for postagens in postagens
    ]
    return {'posts': post_by_name}


@router.put('/{post_id}', status_code=HTTPStatus.OK, response_model=Post)
def update_post(
    post_id: int,
    post: UpdatePostRequest,
    db: Session = Depends(get_session),
):
    postagem = db.query(Post).filter(Post.id == post_id).first()

    if not postagem:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Postagem'),
        )

    categoria = (
        db.query(Category).filter(Category.id == post.id_categoria).all()
    )

    if not categoria:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=get_not_found_message('Categoria'),
        )

    organizacao = (
        db.query(Organization)
        .filter(Organization.id == post.id_organizacao)
        .all()
    )

    if not organizacao:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=get_not_found_message('Organização'),
        )

    usuario = db.query(User).filter(User.id == post.id_usuario).all()

    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=get_not_found_message('Usuário'),
        )

    post_atualizado = Post.update(postagem, post.dict())

    try:
        db.commit()
        db.refresh(post_atualizado)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)

        match = re.search(
            r'UNIQUE constraint failed: posts\.(\w+)', error_message
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
                detail=get_update_error_message('post'),
            )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=get_unexpected_error_message(
                'atualizar a postagem', str(e)
            ),
        )
    return UpdatePostResponse(
        message=get_success_message('Postagem atualizada')
    )


@router.delete(
    '/{post_id}',
    status_code=HTTPStatus.OK,
    response_model=DeletePostResponse,
)
def delete_post(post_id: int, db: Session = Depends(get_session)):
    postagem = db.query(Post).filter(Post.id == post_id).first()

    if not postagem:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Postagem'),
        )

    try:
        db.delete(postagem)
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
                detail=get_conflict_message('postagem'),
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=get_deletion_error_message('postagem'),
            )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=get_unexpected_error_message('deletar a postagem', str(e)),
        )
    return DeletePostResponse(message=get_success_message('Postagem deletada'))
