import re
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_rafa.database import get_session
from fast_rafa.models.message_it import MessageItem
from fast_rafa.models.user import User

router = APIRouter()


@router.post('/', status_code=HTTPStatus.CREATED, response_model=MessageItem)
def create_message_item(
    message_item: MessageItem.Create, db: Session = Depends(get_session)
):
    usuario_um = (
        db.query(User).filter(User.id == message_item.usuario_um).first()
    )
    usuario_dois = (
        db.query(User).filter(User.id == message_item.usuario_dois).first()
    )

    if not usuario_um or not usuario_dois:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Um ou ambos os usuários não foram encontrados',
        )

    novo_message_item = MessageItem.create(message_item)
    try:
        db.add(novo_message_item)
        db.commit()
        db.refresh(novo_message_item)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)

        match = re.search(
            r'UNIQUE constraint failed: message_its\.(\w+)', error_message
        )
        if match:
            field_name = match.group(1).replace('_', ' ').capitalize()
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Já existe um item de mensagem'
                f'com este(a) {field_name}.',
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail='Erro ao criar o item de mensagem.',
            )

    return novo_message_item


@router.get('/', status_code=HTTPStatus.OK, response_model=List[MessageItem])
def read_message_items(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_session)
):
    message_items = db.query(MessageItem).offset(skip).limit(limit).all()

    if not message_items:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Nenhum item de mensagem encontrado!',
        )
    return message_items


@router.get(
    '/{message_item_id}', status_code=HTTPStatus.OK, response_model=MessageItem
)
def read_message_item_by_id(
    message_item_id: int, db: Session = Depends(get_session)
):
    message_item = (
        db.query(MessageItem).filter(MessageItem.id == message_item_id).first()
    )

    if not message_item:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Item de mensagem não encontrado!',
        )
    return message_item


@router.get(
    '/user/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=List[MessageItem],
)
def read_message_items_by_user(
    user_id: int, db: Session = Depends(get_session)
):
    message_items = (
        db.query(MessageItem)
        .filter(
            (MessageItem.usuario_um == user_id)
            | (MessageItem.usuario_dois == user_id)
        )
        .all()
    )

    if not message_items:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Nenhum item de mensagem encontrado para este usuário!',
        )
    return message_items


@router.get(
    '/conversation/{user_one}/{user_two}',
    status_code=HTTPStatus.OK,
    response_model=List[MessageItem],
)
def read_conversation(
    user_one: int, user_two: int, db: Session = Depends(get_session)
):
    message_items = (
        db.query(MessageItem)
        .filter(
            (
                (MessageItem.usuario_um == user_one)
                & (MessageItem.usuario_dois == user_two)
            )
            | (
                (MessageItem.usuario_um == user_two)
                & (MessageItem.usuario_dois == user_one)
            )
        )
        .all()
    )

    if not message_items:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Nenhuma conversa encontrada entre estes usuários!',
        )
    return message_items


@router.put(
    '/{message_item_id}', status_code=HTTPStatus.OK, response_model=MessageItem
)
def update_message_item(
    message_item_id: int,
    message_item_data: MessageItem.UpdateRequest,
    db: Session = Depends(get_session),
):
    message_item = (
        db.query(MessageItem).filter(MessageItem.id == message_item_id).first()
    )

    if not message_item:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Item de mensagem não encontrado!',
        )

    if message_item_data.usuario_um:
        usuario_um = (
            db.query(User)
            .filter(User.id == message_item_data.usuario_um)
            .first()
        )
        if not usuario_um:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Usuário um não encontrado',
            )

    if message_item_data.usuario_dois:
        usuario_dois = (
            db.query(User)
            .filter(User.id == message_item_data.usuario_dois)
            .first()
        )
        if not usuario_dois:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Usuário dois não encontrado',
            )

    message_item = MessageItem.update(
        message_item, message_item_data.dict(exclude_unset=True)
    )

    try:
        db.commit()
        db.refresh(message_item)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)

        match = re.search(
            r'UNIQUE constraint failed: message_its\.(\w+)', error_message
        )
        if match:
            field_name = match.group(1).replace('_', ' ').capitalize()
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Já existe um item de mensagem'
                f'com este(a) {field_name}.',
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail='Erro ao atualizar o item de mensagem.',
            )

    return message_item


@router.delete(
    '/{message_item_id}',
    status_code=HTTPStatus.OK,
    response_model=MessageItem.DeleteResponse,
)
def delete_message_item(
    message_item_id: int, db: Session = Depends(get_session)
):
    message_item = (
        db.query(MessageItem).filter(MessageItem.id == message_item_id).first()
    )

    if not message_item:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Item de mensagem não encontrado!',
        )

    try:
        db.delete(message_item)
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
                    'Não é possível excluir o item de mensagem, '
                    'pois está associado a outros registros.'
                ),
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail='Erro ao excluir o item de mensagem.',
            )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Erro inesperado ao excluir o item de mensagem: {str(e)}',
        )

    return MessageItem.DeleteResponse(
        message='Item de mensagem excluído com sucesso.'
    )
