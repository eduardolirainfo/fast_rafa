import re
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_rafa.core.database import get_session
from fast_rafa.modules.organizations.models import Organization
from fast_rafa.modules.organizations.schemas import (
    OrganizationCreate,
    OrganizationDeleteResponse,
    OrganizationResponse,
    OrganizationUpdateRequest,
    OrganizationUpdateResponse,
)
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


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=OrganizationResponse
)
def create_organization(
    organizacao: OrganizationCreate,
    db: Session = Depends(get_session),
):
    novo_organizacao_data = organizacao.dict()
    novo_organizacao = Organization.create(
        OrganizationCreate(**novo_organizacao_data)
    )
    try:
        db.add(novo_organizacao)
        db.commit()
        db.refresh(novo_organizacao)
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

    return OrganizationResponse.from_home(novo_organizacao)


@router.get('/', response_model=dict, status_code=HTTPStatus.OK)
def read_organizations(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_session)
):
    organizacoes = db.query(Organization).offset(skip).limit(limit).all()

    if not organizacoes:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Organização'),
        )

    lista_organizacoes = [
        OrganizationResponse.from_home(organizacao)
        for organizacao in organizacoes
    ]
    return {'organizacoes': lista_organizacoes}


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

    return OrganizationResponse.from_home(organizacao)


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

    return OrganizationResponse.from_home(organizacao)


@router.get(
    '/name/{organization_by_name}',
    status_code=HTTPStatus.OK,
    response_model=dict,
)
def read_organization_by_name(
    organization_by_name: str, db: Session = Depends(get_session)
):
    organizacoes = get_by_sel(
        db,
        Organization,
        filters={
            'joins': {},
            'filter_plus': {},
            'like_filters': {
                'nome': organization_by_name,
            },
        },
    ).all()

    if not organizacoes:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Nenhuma Organização'),
        )

    lista_organizacoes = [
        OrganizationResponse.from_home(organizacao)
        for organizacao in organizacoes
    ]
    return {'organizacoes': lista_organizacoes}


@router.put(
    '/{organization_id}',
    status_code=HTTPStatus.OK,
    response_model=OrganizationUpdateResponse,
)
def update_organization(
    organization_id: int,
    organization_data: OrganizationUpdateRequest,
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
    update_data = organization_data.dict()
    organizacao = Organization.update(organizacao, update_data)

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

    return OrganizationUpdateResponse.from_home(organizacao)


@router.delete(
    '/{organization_id}',
    status_code=HTTPStatus.OK,
    response_model=OrganizationDeleteResponse,
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
                detail=get_deletion_error_message('organização'),
            )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=get_unexpected_error_message(
                'deletar a organização', str(e)
            ),
        )

    return OrganizationDeleteResponse(
        message=get_success_message('Organização excluída')
    )
