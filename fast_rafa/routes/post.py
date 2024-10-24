import re
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_rafa.database import get_session
from fast_rafa.models.category import Category
from fast_rafa.models.organization import Organization
from fast_rafa.models.post import Post
from fast_rafa.models.user import User

router = APIRouter()


@router.post('/', status_code=HTTPStatus.CREATED, response_model=Post)
def create_post(
    post: Post.Create,
    db: Session = Depends(get_session)
):
    categoria = db.query(Category).filter(
        Category.id == post.id_categoria).all()

    if not categoria:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Categoria não encontrada',
        )

    organizacao = db.query(Organization).filter(
        Organization.id == post.id_organizacao).all()

    if not organizacao:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Organização não encontrada',
        )

    usuario = db.query(User).filter(
        User.id == post.id_usuario).all()

    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Usuário não encontrado',
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
            r'UNIQUE constraint failed: posts\.(\w+)', error_message)
        if match:
            field_name = match.group(1).replace('_', ' ').capitalize()
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=f"Já existe um post com este(a) {field_name}."
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Erro ao criar o post."
            )

    return nova_postagem


# @router.get('/', status_code=HTTPStatus.OK, response_model=list[Post])
# def read_posts(
#     skip: int = 0,
#     limit: int = 10,
#     db: Session = Depends(get_session)
# ):
#     postagens = db.query(
#         Post).offset(skip).limit(limit).all()

#     if not postagens:
#         raise HTTPException(
#             status_code=HTTPStatus.NOT_FOUND,
#             detail='Nenhuma postagem encontrada',
#         )

#     return postagens
