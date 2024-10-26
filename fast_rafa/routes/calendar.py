
import re
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_rafa.database import get_session
from fast_rafa.models.calendar import Calendar
from fast_rafa.models.organization import Organization

router = APIRouter()


@router.post('/', status_code=HTTPStatus.CREATED, response_model=Calendar)
def create_calendar(
    calendario: Calendar.Create,
    db: Session = Depends(get_session)
):
    organizacao = db.query(Organization).filter(
        Organization.id == calendario.id_organizacao).first()
    if not organizacao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Organização não encontrada!'
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
            r'UNIQUE constraint failed: calendars\.(\w+)', error_message)
        if match:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Já existe um calendário para essa organização."
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Erro ao criar o calendário."
            )

    return calendario


@router.get('/', response_model=List[Calendar], status_code=HTTPStatus.OK)
def read_calendars(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_session)
):
    calendarios = db.query(
        Calendar).offset(skip).limit(limit).all()

    if not calendarios:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Nenhum calendário encontrado!',
        )
    return calendarios


@router.get('/{calendar_id}',
            response_model=Calendar,
            status_code=HTTPStatus.OK)
def read_calendar_by_id(
    calendar_id: int,
    db: Session = Depends(get_session)
):
    calendario = db.query(Calendar).filter(
        Calendar.id == calendar_id).first()

    if not calendario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Calendário não encontrado!',
        )
    return calendario


@router.get(
    '/organizarion/{organization_id}',
    response_model=List[Calendar],
    status_code=HTTPStatus.OK
)
def read_calendars_by_organization(
    organization_id: int,
    db: Session = Depends(get_session)
):
    calendarios = db.query(Calendar).filter(
        Calendar.id_organizacao == organization_id).all()

    if not calendarios:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Nenhum calendário encontrado!',
        )
    return calendarios


@router.put(
    '/{calendar_id}',
    response_model=Calendar,
    status_code=HTTPStatus.OK
)
def update_calendar(
    calendar_id: int,
    calendario: Calendar.UpdateRequest,
    db: Session = Depends(get_session)
):
    calendario_atual = db.query(Calendar).filter(
        Calendar.id == calendar_id).first()

    if not calendario_atual:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Calendário não encontrado!',
        )

    calendario_atualizado = Calendar.update(
        calendario_atual, calendario.dict())

    try:
        db.commit()
        db.refresh(calendario_atualizado)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)

        match = re.search(
            r'UNIQUE constraint failed: calendars\.(\w+)', error_message)
        if match:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Já existe um calendário para essa organização."
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Erro ao atualizar o calendário."
            )

    return calendario_atualizado
