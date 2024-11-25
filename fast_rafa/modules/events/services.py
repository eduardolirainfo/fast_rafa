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
