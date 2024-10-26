import re

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_rafa.database import get_session
from fast_rafa.models.delivery import Delivery
from fast_rafa.models.organization import Organization
from fast_rafa.models.post import Post
from fast_rafa.models.user import User

router = APIRouter()


@router.post("/", response_model=Delivery.Create)
def create_delivery(
    delivery_data: Delivery.Create,
    db: Session = Depends(get_session)
):

    postagem = db.query(Post).filter(
        Post.id == delivery_data.id_postagem).first()

    if not postagem:
        raise HTTPException(status_code=404, detail="Postagem não encontrada")

    usuario = db.query(User).filter(
        User.id == delivery_data.id_usuario).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    organizacao = db.query(Organization).filter(
        Organization.id == delivery_data.id_organizacao).first()

    if not organizacao:
        raise HTTPException(
            status_code=404, detail="Organização não encontrada")

    delivery = Delivery.create(delivery_data)

    try:
        db.add(delivery)
        db.commit()
        db.refresh(delivery)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)

        match = re.search(
            r'UNIQUE constraint failed: deliveries\.id', error_message
        )
        if match:
            raise HTTPException(
                status_code=409,
                detail="Essa entrega já existe."
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="Erro ao criar a entrega."
            )

    return delivery.to_dict()


@router.get("/{delivery_id}", response_model=Delivery)
def get_delivery(
    delivery_id: int,
    db: Session = Depends(get_session)
):
    delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return delivery.to_dict()


@router.get('/organization/{org_id}', response_model=list[Delivery])
def get_deliveries_by_org(
    org_id: int,
    db: Session = Depends(get_session)
):
    deliveries = db.query(Delivery).filter(
        Delivery.id_organizacao == org_id).all()
    if not deliveries:
        raise HTTPException(status_code=404, detail="Entregas não encontradas")
    return [delivery.to_dict() for delivery in deliveries]


@router.get('/user/{user_id}', response_model=list[Delivery])
def get_deliveries_by_user(
    user_id: int,
    db: Session = Depends(get_session)
):
    deliveries = db.query(Delivery).filter(
        Delivery.id_usuario == user_id).all()
    if not deliveries:
        raise HTTPException(status_code=404, detail="Entregas não encontradas")
    return [delivery.to_dict() for delivery in deliveries]


@router.get('/post/{post_id}', response_model=list[Delivery])
def get_deliveries_by_post(
    post_id: int,
    db: Session = Depends(get_session)
):
    deliveries = db.query(Delivery).filter(
        Delivery.id_postagem == post_id).all()
    if not deliveries:
        raise HTTPException(status_code=404, detail="Entregas não encontradas")
    return [delivery.to_dict() for delivery in deliveries]


@router.get('/ong/{ong_id}', response_model=list[Delivery])
def get_deliveries_by_ong(
    ong_id: int,
    db: Session = Depends(get_session)
):
    deliveries = db.query(Delivery).filter(
        Delivery.id_ong == ong_id).all()
    if not deliveries:
        raise HTTPException(status_code=404, detail="Entregas não encontradas")
    return [delivery.to_dict() for delivery in deliveries]


@router.put(
    '/{delivery_id}',
    response_model=Delivery.UpdateResponse
)
def update_delivery(
    delivery_id: int,
    delivery_data: Delivery.UpdateRequest,
    db: Session = Depends(get_session)
):
    postagem = db.query(Post).filter(
        Post.id == delivery_data.id_postagem).first()

    if not postagem:
        raise HTTPException(status_code=404, detail="Postagem não encontrada")

    usuario = db.query(User).filter(
        User.id == delivery_data.id_usuario).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    organizacao = db.query(Organization).filter(
        Organization.id == delivery_data.id_organizacao).first()

    if not organizacao:
        raise HTTPException(
            status_code=404, detail="Organização não encontrada")

    entrega = db.query(Delivery).filter(Delivery.id == delivery_id).first()

    if not entrega:
        raise HTTPException(status_code=404, detail="Entrega não encontrada")

    entrega_atualizada = Delivery.update(entrega, delivery_data.dict())

    try:
        db.commit()
        db.refresh(entrega_atualizada)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)

        match = re.search(
            r'UNIQUE constraint failed: deliveries\.id', error_message
        )
        if match:
            raise HTTPException(
                status_code=409,
                detail="Essa entrega já existe."
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="Erro ao criar a entrega."
            )

    return Delivery.UpdateResponse(
        message=(
            'Entrega atualizada com sucesso'
        )
    )


@router.delete("/deliveries/{id}", response_model=Delivery.DeleteRequest)
def delete_delivery(
    id: int,
    db: Session = Depends(get_session)
):
    delivery = db.query(Delivery).filter(Delivery.id == id).first()
    if not delivery:
        raise HTTPException(status_code=404, detail="Entrega não encontrada")
    db.delete(delivery)
    db.commit()
    return {"message": "Entrega deletada com sucesso"}
