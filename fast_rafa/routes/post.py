from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from fast_rafa.schemas.post import (
    PostCreate,
    PostDeleteResponse,
    PostInDB,
    PostUpdate,
)

router = APIRouter()

# Banco de dados em memória
database = []


@router.post('/', status_code=HTTPStatus.CREATED, response_model=PostInDB)
def create_post(post: PostCreate):
    post_db = PostInDB(
        id=len(database) + 1,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        **post.model_dump(),
    )
    database.append(post_db)
    return post_db


@router.get('/', status_code=HTTPStatus.OK, response_model=PostInDB)
def read_posts():
    return database


@router.get('/{post_id}', status_code=HTTPStatus.OK, response_model=PostInDB)
def read_post(post_id: int):
    if post_id <= 0 or post_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Post não encontrado'
        )
    return database[post_id - 1]


@router.put('/{post_id}', status_code=HTTPStatus.OK, response_model=PostInDB)
def update_post(post_id: int, post: PostUpdate):
    if post_id <= 0 or post_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Post não encontrado'
        )

    post_db = PostInDB(
        id=post_id,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        **post.model_dump(exclude_unset=True),
    )
    database[post_id - 1] = post_db
    return post_db


@router.delete(
    '/{post_id}', status_code=HTTPStatus.OK, response_model=PostDeleteResponse
)
def delete_post(post_id: int):
    if post_id <= 0 or post_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Post não encontrado'
        )

    post = database.pop(post_id - 1)
    return PostDeleteResponse(id=post.id, title=post.title)
