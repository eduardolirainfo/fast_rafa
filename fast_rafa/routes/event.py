import re
from http import HTTPStatus
from typing import List

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
from fast_rafa.models.event import Event
from fast_rafa.models.organization import Organization
from fast_rafa.models.user import User

router = APIRouter()


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=Event.CreateEvent
)
def create_event(event: Event.CreateEvent, db: Session = Depends(get_session)):
    organizacao = (
        db.query(Organization)
        .filter(Organization.id == event.id_organizacao)
        .first()
    )

    if not organizacao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Organização'),
        )

    usuario = db.query(User).filter(User.id == event.id_usuario).first()

    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Usuário'),
        )

    novo_evento = Event.create(event)

    try:
        db.add(novo_evento)
        db.commit()
        db.refresh(novo_evento)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)

        match = re.search(
            r'UNIQUE constraint failed:  events\.(\w+)', error_message
        )
        if match:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=get_conflict_message('evento'),
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=get_creation_error_message('evento'),
            )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=get_creation_error_message('evento', str(e)),
        )

    return novo_evento


@router.get('/', status_code=HTTPStatus.OK, response_model=List[Event])
def get_events(db: Session = Depends(get_session)):
    eventos = db.query(Event).all()

    if not eventos:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Eventos'),
        )
    return eventos


@router.put(
    '/{event_id}',
    status_code=HTTPStatus.OK,
    response_model=Event.UpdateResponseEvent,
)
def update_event(
    event_id: int,
    event_data: Event.UpdateRequestEvent,
    db: Session = Depends(get_session),
):
    evento = db.query(Event).filter(Event.id == event_id).first()

    if not evento:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Evento'),
        )

    try:
        evento = Event.update(evento, event_data.dict(exclude_unset=True))
        db.commit()
        db.refresh(evento)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)

        match = re.search(
            r'UNIQUE constraint failed:  events\.(\w+)', error_message
        )

        if match:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=get_conflict_message('evento'),
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=get_update_error_message('evento'),
            )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=get_unexpected_error_message('atualizar evento', str(e)),
        )

    return Event.UpdateResponseEvent(
        message=get_success_message('Evento atualizado')
    )


@router.delete(
    '/{event_id}',
    status_code=HTTPStatus.OK,
)
def delete_event(event_id: int, db: Session = Depends(get_session)):
    evento = db.query(Event).filter(Event.id == event_id).first()

    if not evento:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Evento'),
        )

    try:
        db.delete(evento)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=get_deletion_error_message('evento', str(e)),
        )

    return Event.DeleteResponseEvent(
        message=get_success_message('Evento excluído')
    )
