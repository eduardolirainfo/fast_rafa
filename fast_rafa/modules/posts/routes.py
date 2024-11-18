import re
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_rafa.core.database import get_session
from fast_rafa.core.security import get_current_user
from fast_rafa.modules.categories.models import Category
from fast_rafa.modules.organizations.models import Organization
from fast_rafa.modules.posts.models import Post
from fast_rafa.modules.posts.schemas import (
    CreatePost,
    DeletePostResponse,
    PostResponse,
    UpdatePostRequest,
    UpdatePostResponse,
)
from fast_rafa.modules.users.models import User
from fast_rafa.utils.error_messages import (
    get_conflict_message,
    get_creation_error_message,
    get_deletion_error_message,
    get_not_found_message,
    get_success_message,
    get_unexpected_error_message,
    get_update_error_message,
)
from fast_rafa.utils.sel import get_by_sel

router = APIRouter()


@router.post('/', status_code=HTTPStatus.CREATED, response_model=dict)
def create_post(post: CreatePost, db: Session = Depends(get_session)):
    categoria = get_by_sel(
        db,
        Category,
        filters={
            'filter_plus': {'id': post.id_categoria},
        },
    ).first()

    if not categoria:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=get_not_found_message('Categoria'),
        )

    organizacao = get_by_sel(
        db,
        Organization,
        filters={
            'joins': {},
            'filter_plus': {'id': post.id_organizacao},
            'like_filters': {},
        },
    ).first()

    if not organizacao:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=get_not_found_message('Organização'),
        )

    usuario = get_by_sel(
        db,
        User,
        filters={
            'joins': {},
            'filter_plus': {'id': post.id_usuario},
            'like_filters': {},
        },
    ).first()

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
    novo_post = PostResponse.from_orm(nova_postagem).to_dict()
    return novo_post


@router.get('/', status_code=HTTPStatus.OK, response_model=list[PostResponse])
def read_posts(
    skip: int = 0,
    limit: int = 10,
    status: int = None,
    order_by: str = 'titulo',
    db: Session = Depends(get_session),
):
    filters = {}
    if status is not None:
        filters['status'] = status

    ALLOWED_SORT_FIELDS = {
        'titulo',
        'descricao',
        'status',
        'data_validade',
        'criado_em',
        'atualizado_em',
    }

    if order_by not in ALLOWED_SORT_FIELDS:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Campo de ordenação inválido.',
        )
    postagens = (
        get_by_sel(db, Post, filters={'filter_plus': filters})
        .order_by(order_by)
        .offset(skip)
        .limit(limit)
        .all()
    )

    if not postagens:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Postagem'),
        )

    postagens = [PostResponse.from_home(post) for post in postagens]

    return postagens


@router.get('/export', status_code=HTTPStatus.OK)
def export_posts(db: Session = Depends(get_session)):
    postagens = get_by_sel(db, Post, filters={}).all()
    return {'posts': [PostResponse.from_home(post) for post in postagens]}


@router.get('/stats', status_code=HTTPStatus.OK)
def get_post_stats(db: Session = Depends(get_session)):
    stats = (
        db.query(Post.status, func.count(Post.id)).group_by(Post.status).all()
    )
    return {'stats': dict(stats)}


@router.get(
    '/{post_id}', status_code=HTTPStatus.OK, response_model=PostResponse
)
def read_post_by_id(post_id: int, db: Session = Depends(get_session)):
    postagem = get_by_sel(
        db, Post, filters={'filter_plus': {'id': post_id}}
    ).first()

    if not postagem:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Postagem'),
        )
    post = PostResponse.from_home(postagem)
    return post


@router.get(
    '/name/{post_name}',
    status_code=HTTPStatus.OK,
    response_model=list[PostResponse],
)
def read_post_by_name(
    post_name: str,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    filters = {
        'filter_plus': {'status': 1},
        'like_filters': {'titulo': post_name, 'descricao': post_name},
    }

    postagens = (
        get_by_sel(db=db, model=Post, filters=filters)
        .offset(skip)
        .limit(limit)
        .all()
    )

    if not postagens:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Postagem'),
        )

    post_by_name = [PostResponse.from_home(post) for post in postagens]
    return post_by_name


@router.put('/{post_id}', status_code=HTTPStatus.OK, response_model=Post)
def update_post(
    post_id: int,
    post: UpdatePostRequest,
    db: Session = Depends(get_session),
):
    postagem = get_by_sel(
        db,
        Post,
        filters={'filter_plus': {'id': post_id}},
    ).first()

    if not postagem:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Postagem'),
        )

    categoria = get_by_sel(
        db,
        Category,
        filters={'filter_plus': {'id': post.id_categoria}},
    ).first()

    if not categoria:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=get_not_found_message('Categoria'),
        )

    organizacao = get_by_sel(
        db,
        Organization,
        filters={'filter_plus': {'id': post.id_organizacao}},
    ).first()

    if not organizacao:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=get_not_found_message('Organização'),
        )

    usuario = get_by_sel(
        db,
        User,
        filters={'filter_plus': {'id': post.id_usuario}},
    ).first()

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


@router.patch('/{post_id}/status', status_code=HTTPStatus.OK)
def update_post_status(
    post_id: int,
    status: bool,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    if not isinstance(status, bool):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='O status deve ser um valor booleano.',
        )

    if status:
        status = 1
    else:
        status = 0

    postagem = get_by_sel(
        db,
        Post,
        filters={
            'filter_plus': {'id': post_id, 'id_usuario': current_user.id}
        },
    ).first()

    if not postagem:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Postagem não existe e/ou '
            'você não tem permissão para atualizá-la.',
        )

    if postagem.status == status:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='O status da postagem já está atualizado.',
        )

    postagem.status = status
    db.commit()
    return UpdatePostResponse(
        message=get_success_message('Postagem atualizada')
    )


@router.delete(
    '/{post_id}',
    status_code=HTTPStatus.OK,
    response_model=DeletePostResponse,
)
def delete_post(post_id: int, db: Session = Depends(get_session)):
    postagem = get_by_sel(
        db,
        Post,
        filters={'filter_plus': {'id': post_id}},
    ).first()

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
