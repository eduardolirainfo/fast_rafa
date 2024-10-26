import re
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_rafa.database import get_session
from fast_rafa.models.event import Event

router = APIRouter()


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=Event.Create)
def create_event(
    event: Event.Create,
    db: Session = Depends(get_session)
):
    novo_evento = Event.create(event)

    try:
        db.add(novo_evento)
        db.commit()
        db.refresh(novo_evento)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)

        if 'UNIQUE constraint failed' in error_message:
            match = re.search(
                r'UNIQUE constraint failed: events\.(\w+)',
                error_message)
            if match:
                field_name = match.group(1).replace('_', ' ').capitalize()
                raise HTTPException(
                    status_code=HTTPStatus.CONFLICT,
                    detail=f"Já existe um evento com este(a) {field_name}."
                )
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Erro ao criar o evento."
        )

    return novo_evento


@router.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=List[Event]
)
def get_events(
    db: Session = Depends(get_session)
):
    eventos = db.query(Event).all()

    if not eventos:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Nenhum evento encontrado!'
        )
    return eventos


@router.get(
    '/{event_id}',
    status_code=HTTPStatus.OK,
    response_model=Event
)
def get_event(
    event_id: int,
    db: Session = Depends(get_session)
):
    evento = db.query(Event).filter(Event.id == event_id).first()

    if not evento:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Evento não encontrado!'
        )
    return evento


@router.get(
    '/user/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=List[Event]
)
def get_events_by_user(
    user_id: int,
    db: Session = Depends(get_session)
):
    eventos = db.query(Event).filter(Event.id_usuario == user_id).all()

    if not eventos:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Nenhum evento encontrado!'
        )
    return eventos


@router.get(
    '/organization/{organization_id}',
    status_code=HTTPStatus.OK,
    response_model=List[Event]
)
def get_events_by_organization(
    organization_id: int,
    db: Session = Depends(get_session)
):
    eventos = db.query(Event).filter(
        Event.id_organizacao == organization_id).all()

    if not eventos:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Nenhum evento encontrado!'
        )
    return eventos


@router.put(
    '/{event_id}',
    status_code=HTTPStatus.OK,
    response_model=Event.UpdateResponse
)
def update_event(
    event_id: int,
    event_data: Event.UpdateRequest,
    db: Session = Depends(get_session)
):
    evento = db.query(Event).filter(Event.id == event_id).first()

    if not evento:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Evento não encontrado!'
        )

    try:
        evento = Event.update(evento, event_data.dict(exclude_unset=True))
        db.commit()
        db.refresh(evento)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)

        if ('unique constraint' in error_message.lower()):
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Já existe um evento com os mesmos dados."
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Erro ao atualizar o evento."
            )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Erro inesperado ao atualizar o evento: {str(e)}"
        )

    return Event.UpdateResponse(
        message="Evento atualizado com sucesso."
    )


@router.delete(
    '/{event_id}',
    status_code=HTTPStatus.OK,
    response_model=Event.DeleteResponse
)
def delete_event(
    event_id: int,
    db: Session = Depends(get_session)
):
    evento = db.query(Event).filter(Event.id == event_id).first()

    if not evento:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Evento não encontrado!'
        )

    try:
        db.delete(evento)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)

        if ('foreign key constraint' in error_message.lower() or
                'constraint failed' in error_message.lower()):
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=(
                    "Não é possível excluir o evento, "
                    "pois está associado a outros registros."
                ),
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Erro ao excluir o evento."
            )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f"Erro inesperado ao excluir o evento: {str(e)}"
        )

    return Event.DeleteResponse(
        message="Evento excluído com sucesso."
    )
