import re
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_rafa.core.database import get_session
from fast_rafa.modules.events.models import Event
from fast_rafa.modules.events.schemas import (
    EventCreate,
    EventDeleteResponse,
    EventResponse,
    EventUpdateRequest,
    EventUpdateResponse,
)
from fast_rafa.modules.organizations.models import Organization
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


@router.post('/', status_code=HTTPStatus.CREATED, response_model=EventResponse)
def create_event(evento: EventCreate, db: Session = Depends(get_session)):
    organizacao = get_by_sel(
        db,
        Organization,
        filters={
            'filter_plus': {'id': evento.id_organizacao},
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
            'filter_plus': {'id': evento.id_usuario},
        },
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=get_not_found_message('Usuário'),
        )

    novo_evento_data = evento.dict()
    novo_evento = Event.create(EventCreate(**novo_evento_data))
    try:
        db.add(novo_evento)
        db.commit()
        db.refresh(novo_evento)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)

        match = re.search(
            r'UNIQUE constraint failed: events\.(\w+)', error_message
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
                detail=get_creation_error_message('evento'),
            )

    return EventResponse.from_home(novo_evento)


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
    response_model=EventUpdateResponse,
)
def update_event(
    event_id: int,
    event_data: EventUpdateRequest,
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

    return EventUpdateResponse(
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

    return EventDeleteResponse(message=get_success_message('Evento excluído'))
