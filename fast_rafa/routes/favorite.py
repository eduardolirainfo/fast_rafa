from datetime import datetime
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, HTTPException

from fast_rafa.models.favorite import Favorite
from fast_rafa.models.post import Post
from fast_rafa.models.user import User

router = APIRouter()


@router.post(
    '/{id_usuario}/{id_postagem}',
    status_code=HTTPStatus.CREATED,
    response_model=Favorite,
)
def create_favorite(id_usuario: int, id_postagem: int):

    # Verifica o tipo e o conteúdo dos itens no banco de dados
    for item in table_registry:
        print(f'Item: {item}, Tipo: {type(item)}')

    # Verifica se o usuário existe
    user_exists = any(
        user.id == id_usuario
        for user in table_registry
        if isinstance(user, User)
    )
    print(f'Usuário encontrado: {user_exists}')
    if not user_exists:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Usuário com id {id_usuario} não encontrado',
        )

    # Verifica se a postagem existe
    post_exists = any(
        post.id == id_postagem
        for post in table_registry
        if isinstance(post, Post)
    )
    print(f'Postagem encontrada: {post_exists}')
    if not post_exists:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Postagem com id {id_postagem} não encontrada',
        )

    # Cria um novo favorito
    favorite_db = Favorite(
        id=len(table_registry) + 1,
        idusuario=id_usuario,
        idpostagem=id_postagem,
        criado_em=datetime.utcnow(),
        atualizado_em=datetime.utcnow(),
    )

    # Adiciona o favorito ao banco de dados
    table_registry.append(favorite_db)
    return favorite_db


@router.get('/', status_code=HTTPStatus.OK, response_model=List[Favorite])
def read_favorites():
    return table_registry


@router.get(
    '/{favorite_id}', status_code=HTTPStatus.OK, response_model=Favorite
)
def read_favorite(favorite_id: int):
    if favorite_id <= 0 or favorite_id > len(table_registry):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Favorito não encontrado'
        )
    return table_registry[favorite_id - 1]


@router.put(
    '/{favorite_id}', status_code=HTTPStatus.OK, response_model=Favorite
)
def update_favorite(favorite_id: int, favorite: Favorite):
    # Verifica se o id do favorito é válido
    if favorite_id < 1 or favorite_id > len(table_registry):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Favorito não encontrado'
        )

    existing_favorite = table_registry[favorite_id - 1]
    updated_data = favorite.model_dump(exclude_unset=True)
    updated_favorite = existing_favorite.copy(update=updated_data)
    updated_favorite.atualizado_em = datetime.utcnow()

    table_registry[favorite_id - 1] = updated_favorite

    return updated_favorite


@router.delete('/{favorite_id}', response_model=Favorite)
def delete_favorite(favorite_id: int):
    if favorite_id < 1 or favorite_id > len(table_registry):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Favorito não encontrado'
        )
    deleted_favorite = table_registry.pop(favorite_id - 1)
    return deleted_favorite
