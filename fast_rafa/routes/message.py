from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from fast_rafa.database import get_session
from fast_rafa.messages.error_messages import (
    get_deletion_error_message,
    get_not_found_message,
    get_success_message,
    get_unexpected_error_message,
)
from fast_rafa.models.message import Message
from fast_rafa.models.message_it import MessageItem
from fast_rafa.security import get_current_user

router = APIRouter()


@router.get('/', response_model=List[MessageItem])
def get_messages(
    db: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user),
):
    mensagens_conversa = (
        db.query(MessageItem)
        .filter(
            (MessageItem.usuario_um == current_user_id)
            | (MessageItem.usuario_dois == current_user_id)
        )
        .all()
    )
    return mensagens_conversa


@router.get('/{id}', response_model=Message)
def get_message(
    id: int,
    db: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user),
):
    message = db.query(Message).get(id)
    if message and current_user_id in {
        message.id_remetente,
        message.message_it.usuario_dois,
    }:
        return message
    raise HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Você não tem autorização para visualizar esta mensagem.',
    )


@router.post('/', response_model=MessageItem, status_code=HTTPStatus.CREATED)
def create_conversation(
    message_data: Message.CreateMessage,
    db: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user),
):
    nova_conversa = MessageItem.create(
        usuario_um=current_user_id, usuario_dois=message_data.id_remetente
    )

    try:
        message = Message.create(message_data)
        db.add(message)
        db.commit()
        db.refresh(message)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=get_unexpected_error_message('criar mensagem', str(e)),
        )

    return nova_conversa


@router.post('/reply', response_model=Message, status_code=HTTPStatus.CREATED)
def reply_to_conversation(
    message_data: Message.CreateMessage,
    db: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user),
):
    mensagem = (
        db.query(MessageItem)
        .filter(
            (MessageItem.usuario_um == current_user_id)
            & (MessageItem.usuario_dois == message_data.id_remetente)
        )
        .first()
    )

    if not mensagem:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Mensagem'),
        )

    try:
        message = Message.create(message_data)
        db.add(message)
        db.commit()
        db.refresh(message)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=get_unexpected_error_message('responder mensagem', str(e)),
        )
    return message


@router.put('/{id}', response_model=Message)
def update_message(
    id: int,
    message_data: Message.UpdateRequest,
    db: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user),
):
    message = db.query(Message).get(id)
    if not message or message.id_remetente != current_user_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Você não tem' 'autorização para editar esta mensagem.',
        )

    message.conteudo = message_data.conteudo
    message.url_imagem = message_data.url_imagem

    try:
        db.commit()
        db.refresh(message)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=get_unexpected_error_message('mensagem', str(e)),
        )

    return Message.UpdateResponseMessage(
        message=get_success_message('Mensagem atualizada')
    )


@router.delete('/{id}', response_model=MessageItem)
def delete_message(
    id: int,
    db: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user),
):
    message = db.query(Message).get(id)
    if not message:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Mensagem'),
        )

    id_conversa = message.id_mensagem_it

    try:
        db.delete(message)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=get_deletion_error_message('mensagem', str(e)),
        )
    conversa = db.query(MessageItem).get(id_conversa)
    return conversa


@router.delete('/conversations/{id}', response_model=dict)
def delete_conversation(
    id: int,
    db: Session = Depends(get_session),
    current_user_id: int = Depends(get_current_user),
):
    conversa = db.query(MessageItem).get(id)
    if not conversa:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Conversa'),
        )

    try:
        db.delete(conversa)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=get_deletion_error_message('conversa', str(e)),
        )

    return Message.DeleteResponseMessage(
        message=get_success_message('Conversa excluída')
    )
