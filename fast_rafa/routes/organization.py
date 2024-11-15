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
from fast_rafa.models.organization import Organization

router = APIRouter()


@router.post('/', status_code=HTTPStatus.CREATED, response_model=Organization)
def create_organization(
    organizacao: Organization.CreateOrganization,
    db: Session = Depends(get_session),
):
    organizacao = Organization.create(organizacao)
    try:
        db.add(organizacao)
        db.commit()
        db.refresh(organizacao)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)

        match = re.search(
            r'UNIQUE constraint failed: organizations\.(\w+)', error_message
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
                detail=get_creation_error_message('organização'),
            )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=get_unexpected_error_message('criar organização', str(e)),
        )

    return organizacao


@router.get('/', response_model=List[Organization], status_code=HTTPStatus.OK)
def read_organizations(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_session)
):
    organizacoes = db.query(Organization).offset(skip).limit(limit).all()

    if not organizacoes:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Organização'),
        )

    return [organizacao.to_dict() for organizacao in organizacoes]


@router.get('/{organization_id}', status_code=HTTPStatus.OK)
def read_organization_by_id(
    organization_id: int, db: Session = Depends(get_session)
):
    organizacao = (
        db.query(Organization)
        .filter(Organization.id == organization_id)
        .first()
    )

    if not organizacao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Organização'),
        )

    return organizacao.to_dict()


@router.get('/federal/{organization_id_federal}', status_code=HTTPStatus.OK)
def read_organization_by_id_federal(
    organization_id_federal: str, db: Session = Depends(get_session)
):
    organizacao = (
        db.query(Organization)
        .filter(Organization.id_federal == organization_id_federal)
        .first()
    )

    if not organizacao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Organização'),
        )

    return organizacao.to_dict()


@router.get('/name/{organization_by_name}', status_code=HTTPStatus.OK)
def read_organization_by_name(
    organization_by_name: str, db: Session = Depends(get_session)
):
    organizacao = (
        db.query(Organization)
        .filter(Organization.nome == organization_by_name)
        .first()
    )

    if not organizacao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Organização'),
        )

    return organizacao.to_dict()


@router.put(
    '/{organization_id}',
    status_code=HTTPStatus.OK,
    response_model=Organization.UpdateResponseOrganization,
)
def update_organization(
    organization_id: int,
    organization_data: Organization.UpdateRequestOrganization,
    db: Session = Depends(get_session),
):
    organizacao = (
        db.query(Organization)
        .filter(Organization.id == organization_id)
        .first()
    )

    if not organizacao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Organização'),
        )

    organizacao = Organization.update(organizacao, organization_data.dict())

    try:
        db.commit()
        db.refresh(organizacao)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)

        match = re.search(
            r'UNIQUE constraint failed: organizations\.(\w+)', error_message
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
                detail=get_update_error_message('organização'),
            )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=get_unexpected_error_message(
                'atualizar organização', str(e)
            ),
        )

    return Organization.UpdateResponseOrganization(
        message=get_success_message('Organização atualizada')
    )


@router.delete(
    '/{organization_id}',
    status_code=HTTPStatus.OK,
    response_model=Organization.DeleteResponseOrganization,
)
def delete_organization(
    organization_id: int, db: Session = Depends(get_session)
):
    organizacao = (
        db.query(Organization)
        .filter(Organization.id == organization_id)
        .first()
    )

    if not organizacao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Organização'),
        )

    try:
        db.delete(organizacao)
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
                detail=get_deletion_error_message('organização'),
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=get_deletion_error_message('organização'),
            )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=get_unexpected_error_message(
                'excluir a organização', str(e)
            ),
        )

    return Organization.DeleteResponseOrganization(
        message=get_success_message('Organização excluída')
    )
