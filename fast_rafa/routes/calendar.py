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
from fast_rafa.models.calendar import Calendar
from fast_rafa.models.organization import Organization

router = APIRouter()


@router.post('/', status_code=HTTPStatus.CREATED, response_model=Calendar)
def create_calendar(
    calendario: Calendar.CreateCalendar, db: Session = Depends(get_session)
):
    organizacao = (
        db.query(Organization)
        .filter(Organization.id == calendario.id_organizacao)
        .first()
    )
    if not organizacao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Organização'),
        )

    calendario = Calendar.create(calendario)
    try:
        db.add(calendario)
        db.commit()
        db.refresh(calendario)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)

        match = re.search(
            r'UNIQUE constraint failed: calendars\.(\w+)', error_message
        )
        if match:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=get_conflict_message('Calendário'),
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=get_creation_error_message('Calendário'),
            )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=get_unexpected_error_message('criar calendário', str(e)),
        )

    return calendario


@router.get('/', response_model=List[Calendar], status_code=HTTPStatus.OK)
def read_calendars(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_session)
):
    calendarios = db.query(Calendar).offset(skip).limit(limit).all()

    if not calendarios:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Calendário'),
        )
    return calendarios


@router.get(
    '/{calendar_id}', response_model=Calendar, status_code=HTTPStatus.OK
)
def read_calendar_by_id(calendar_id: int, db: Session = Depends(get_session)):
    calendario = db.query(Calendar).filter(Calendar.id == calendar_id).first()

    if not calendario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Calendário'),
        )
    return calendario


@router.get(
    '/organization/{organization_id}',
    response_model=List[Calendar],
    status_code=HTTPStatus.OK,
)
def read_calendars_by_organization(
    organization_id: int, db: Session = Depends(get_session)
):
    calendarios = (
        db.query(Calendar)
        .filter(Calendar.id_organizacao == organization_id)
        .all()
    )

    if not calendarios:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Calendário'),
        )
    return calendarios


@router.put(
    '/{calendar_id}', response_model=Calendar, status_code=HTTPStatus.OK
)
def update_calendar(
    calendar_id: int,
    calendario: Calendar.UpdateRequestCalendar,
    db: Session = Depends(get_session),
):
    calendario_atual = (
        db.query(Calendar).filter(Calendar.id == calendar_id).first()
    )

    if not calendario_atual:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Calendário'),
        )

    calendario_atualizado = Calendar.update(
        calendario_atual, calendario.dict()
    )

    try:
        db.commit()
        db.refresh(calendario_atualizado)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)

        match = re.search(
            r'UNIQUE constraint failed: calendars\.(\w+)', error_message
        )
        if match:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=get_conflict_message('Calendário'),
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=get_update_error_message('Calendário'),
            )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=get_unexpected_error_message(
                'atualizar calendário', str(e)
            ),
        )

    return Calendar.UpdateResponseCalendar(
        message=get_success_message('Calendário atualizado'),
        calendario=calendario_atualizado,
    )


@router.delete(
    '/{calendar_id}', response_model=dict, status_code=HTTPStatus.OK
)
def delete_calendar(calendar_id: int, db: Session = Depends(get_session)):
    calendario = db.query(Calendar).filter(Calendar.id == calendar_id).first()

    if not calendario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Calendário'),
        )

    try:
        db.delete(calendario)
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
                detail=get_deletion_error_message('Calendário'),
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=get_deletion_error_message('Calendário'),
            )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=get_unexpected_error_message('excluir calendário', str(e)),
        )

    return Calendar.DeleteResponseCalendar(
        message=get_success_message('Calendário excluído')
    )
