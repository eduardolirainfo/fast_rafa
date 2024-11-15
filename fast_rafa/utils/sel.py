from typing import Any, Dict, Optional

from sqlalchemy.orm import Session
from sqlalchemy.sql import or_


def get_by_sel(
    db: Session,
    model: Any,
    current_user_id: Optional[int] = None,
    filter_plus: Optional[Dict[str, Any]] = None,
):
    query = db.query(model)

    if model == 'User':
        # para que o usuário possa ver a si mesmo e não veja usuários deletados
        query = query.filter(
            or_(
                model.eh_deletado.is_(False),
                model.id == current_user_id,
            ),
        )

    if filter_plus:
        for field, value in filter_plus.items():
            if hasattr(model, field):
                query = query.filter(getattr(model, field) == value)
    return query
