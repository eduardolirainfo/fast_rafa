import re
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_rafa.core.database import get_session
from fast_rafa.modules.deliveries.models import Delivery
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

router = APIRouter()


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=Delivery.CreateDelivery
)
def create_delivery(
    delivery: Delivery.CreateDelivery, db: Session = Depends(get_session)
):
    organization = (
        db.query(Organization)
        .filter(Organization.id == delivery.id_organization)
        .first()
    )

    if not organization:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Organização'),
        )

    user = db.query(User).filter(User.id == delivery.id_user).first()

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Usuário'),
        )

    new_delivery = Delivery.create(delivery)

    try:
        db.add(new_delivery)
        db.commit()
        db.refresh(new_delivery)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)

        match = re.search(
            r'UNIQUE constraint failed: deliveries\.(\w+)', error_message
        )

        if match:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=get_conflict_message(match.group(1)),
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=get_creation_error_message('entrega'),
            )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=get_unexpected_error_message('criar a entrega', str(e)),
        )

    return new_delivery


@router.get('/', status_code=HTTPStatus.OK, response_model=List[Delivery])
def get_deliveries(db: Session = Depends(get_session)):
    deliveries = db.query(Delivery).all()

    if not deliveries:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Entrega'),
        )
    return deliveries


@router.put(
    '/{delivery_id}',
    status_code=HTTPStatus.OK,
    response_model=Delivery.UpdateResponseDelivery,
)
def update_delivery(
    delivery_id: int,
    delivery_data: Delivery.UpdateRequestDelivery,
    db: Session = Depends(get_session),
):
    delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()

    if not delivery:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Entrega'),
        )

    try:
        delivery = Delivery.update(
            delivery, delivery_data.dict(exclude_unset=True)
        )
        db.commit()
        db.refresh(delivery)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)

        match = re.search(
            r'UNIQUE constraint failed:  deliveries\.(\w+)', error_message
        )

        if match:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=get_update_error_message('entrega'),
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=get_update_error_message('entrega'),
            )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=get_unexpected_error_message('atualizar a entrega', str(e)),
        )

    return Delivery.UpdateResponseDelivery(
        message=get_success_message('Entrega atualizada')
    )


@router.delete(
    '/{delivery_id}',
    status_code=HTTPStatus.OK,
)
def delete_delivery(delivery_id: int, db: Session = Depends(get_session)):
    delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()

    if not delivery:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=get_not_found_message('Entrega'),
        )

    try:
        db.delete(delivery)
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
                detail=get_deletion_error_message('entrega'),
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=get_deletion_error_message('entrega'),
            )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=get_unexpected_error_message('deletar a entrega', str(e)),
        )

    return Delivery.DeleteResponseDelivery(
        message=get_success_message('Entrega excluída')
    )
