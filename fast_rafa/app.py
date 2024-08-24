from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_rafa.schema import Message
from fast_rafa.user import (
    UserDb,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI()

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olar mundo!'}


@app.post('/users', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_db = UserDb(
        id=len(database) + 1,
        # ** desempacota o dicionário
        **user.model_dump(),
    )
    database.append(user_db)
    return user_db


@app.get('/users', status_code=HTTPStatus.OK, response_model=UserList)
def read_users():
    return {'users': database}


@app.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(user_id: int, user: UserSchema):
    """Update user"""
    if user_id <= 0 or user_id > len(database):
        # raise = Erguer / Lançar / Levantar uma exceção
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )

    user_db = UserDb(id=user_id, **user.model_dump())
    database[user_id - 1] = user_db
    return user_db


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    """Deletar usuário"""
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado',
        )
    del database[user_id - 1]
    return {'message': 'Usuário deletado com sucesso'}


@app.get(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def read_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado',
        )
    return database[user_id - 1]
