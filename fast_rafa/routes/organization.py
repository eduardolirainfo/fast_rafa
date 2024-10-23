import re
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_rafa.database import get_session
from fast_rafa.models.organization import Organization

router = APIRouter()


@router.post('/', status_code=HTTPStatus.CREATED, response_model=Organization)
def create_organization(
    organizacao: Organization.Create,
    db: Session = Depends(get_session)
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
            r'UNIQUE constraint failed: organizations\.(\w+)', error_message)
        if match:
            field_name = match.group(1).replace('_', ' ').capitalize()
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=f"Já existe uma organização com este(a) {field_name}."
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Erro ao criar a organização."
            )

    return organizacao


@router.get('/', response_model=List[Organization], status_code=HTTPStatus.OK)
def read_organizations(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_session)
):
    organizacoes = db.query(
        Organization).offset(skip).limit(limit).all()

    if not organizacoes:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Nenhuma organização encontrada!',
        )

    return [organizacao.to_dict() for organizacao in organizacoes]


@router.get('/{organization_id}', status_code=HTTPStatus.OK)
def read_organization_by_id(
    organization_id: int,
    db: Session = Depends(get_session)
):
    organizacao = db.query(Organization).filter(
        Organization.id == organization_id).first()

    if not organizacao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Organização não encontrada!',
        )

    return organizacao.to_dict()


@router.get('/federal/{organization_id_federal}',
            status_code=HTTPStatus.OK)
def read_organization_by_id_federal(
    organization_id_federal: str,
    db: Session = Depends(get_session)
):
    organizacao = db.query(Organization).filter(
        Organization.id_federal == organization_id_federal).first()

    if not organizacao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Organização não encontrada!',
        )

    return organizacao.to_dict()


@router.get('/name/{organization_by_name}', status_code=HTTPStatus.OK)
def read_organization_by_name(
    organization_by_name: str,
    db: Session = Depends(get_session)
):
    organizacao = db.query(Organization).filter(
        Organization.nome == organization_by_name).first()

    if not organizacao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Organização não encontrada!',
        )

    return organizacao.to_dict()


@router.put('/{organization_id}',
            status_code=HTTPStatus.OK,
            response_model=Organization)
def update_organization(
    organization_id: int,
    organization_data: Organization.UpdateRequest,
    db: Session = Depends(get_session)
):
    organizacao = db.query(Organization).filter(
        Organization.id == organization_id).first()

    if not organizacao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Organização não encontrada!',
        )

    organizacao = Organization.update(organizacao, organization_data.dict())

    try:
        db.commit()
        db.refresh(organizacao)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)

        match = re.search(
            r'UNIQUE constraint failed: organizations\.(\w+)', error_message)
        if match:
            field_name = match.group(1).replace('_', ' ').capitalize()
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=f"Já existe uma organização com este(a) {field_name}."
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Erro ao atualizar a organização."
            )

    return organizacao


@router.delete(
    '/{organization_id}',
    status_code=HTTPStatus.OK,
    response_model=Organization.DeleteResponse,
)
def delete_organization(
    organization_id: int,
    db: Session = Depends(get_session)
):
    organizacao = db.query(Organization).filter(
        Organization.id == organization_id
    ).first()

    if not organizacao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Organização não encontrada!',
        )

    try:
        db.delete(organizacao)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)

        if 'foreign key constraint' in error_message.lower():
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=(
                    "Não é possível excluir a organização, "
                    "pois está associada a outros registros."
                ),
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Erro ao excluir a organização.",
            )

    return Organization.DeleteResponse(
        message="Organização excluída com sucesso.")
