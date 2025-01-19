from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from fast_rafa.modules.events.models import Event
from fast_rafa.modules.organizations.models import Organization
from fast_rafa.modules.users.models import User


def get_suggested_events(db: Session, user_organization_id: int):
    return (
        db.query(Event, func.count(User.id).label('user_count'))
        .join(Organization, Organization.id == Event.id_organizacao)
        .join(User, User.id == Event.id_usuario)
        .filter(
            Event.fechado >= func.now(),
            Event.id_organizacao != user_organization_id,
        )
        .group_by(Event.id)
        .order_by(func.count(User.id).desc())
        .options(joinedload(Event.organization), joinedload(Event.manager))
        .limit(3)
        .all()
    )


def get_events(
    db: Session,
    event_slug: str = None,
    user_organization_id: int = None,
    user_eh_gerente: bool = None,
):
    query = db.query(Event)
    gerente = False
    if user_eh_gerente is not None:
        gerente = user_eh_gerente

    if event_slug:
        query = query.filter(Event.slug == event_slug)
        events = query.first()

        if events:
            events.pode_editar = (
                events.id_organizacao == user_organization_id
            ) and gerente
            return events
        else:
            return []

    else:
        events = query.all()

        result = []
        for event in events:
            pode_editar = (
                event.id_organizacao == user_organization_id
            ) and gerente
            event.pode_editar = pode_editar
            result.append(event)

        return result
