from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session
from sqlalchemy.sql import or_


def handle_joins(query, model, filters, join_type):
    """
    Função para aplicar joins ao modelo com base nos filtros.
    """
    if 'joins' not in filters:
        return query

    for join_model in filters['joins']:
        model_name = join_model.__name__

        field_mapping = {
            'User': 'id_organizacao',
            'Post': ['id_usuario', 'id_categoria', 'id_organizacao'],
            'Message': ['id_remetente', 'id_postagem', 'id_mensagem_it'],
            'Favorite': ['id_usuario', 'id_postagem'],
            'Delivery': [
                'id_usuario',
                'id_postagem',
                'id_organizacao',
                'id_ong',
            ],
            'Event': ['id_usuario', 'id_organizacao'],
            'Watchlist': ['id_organizacao', 'id_usuario'],
            'Calendar': 'id_organizacao',
            'Category': {
                'Post': 'id_categoria'
            },  # Adicionando mapeamento específico para Category
        }

        join_conditions = []

        # Tratamento especial para Category
        if model_name == 'Category' and model.__name__ == 'Post':
            join_conditions = [model.id_categoria == join_model.id]
        else:
            related_fields = field_mapping.get(model_name)
            if isinstance(related_fields, list):
                for field in related_fields:
                    join_conditions.append(
                        getattr(model, 'id') == getattr(join_model, field)
                    )
            elif isinstance(related_fields, dict):
                # Handle dictionary mapping for specific model relationships
                model_specific = related_fields.get(model.__name__)
                if model_specific:
                    join_conditions.append(
                        getattr(model, model_specific)
                        == getattr(join_model, 'id')
                    )
            elif related_fields:
                join_conditions.append(
                    getattr(model, 'id') == getattr(join_model, related_fields)
                )

        if not join_conditions:
            continue  # Skip if no valid join conditions found

        if join_type == 'outerjoin':
            query = query.outerjoin(join_model, or_(*join_conditions))
        else:
            query = query.join(join_model, or_(*join_conditions))

        query = query.add_columns(getattr(join_model, 'id'))

    return query


def apply_filter_plus(query, model, filters):
    """
    Função para aplicar filtros adicionais ('filter_plus') à consulta.
    """
    if 'filter_plus' in filters:
        for field, value in filters['filter_plus'].items():
            if hasattr(model, field):
                query = query.filter(getattr(model, field) == value)
    return query


def apply_like_filters(query, model, filters):
    """
    Função para aplicar filtros do tipo LIKE à consulta.
    """
    if 'like_filters' in filters:
        like_conditions = []
        for field, value in filters['like_filters'].items():
            if hasattr(model, field):
                like_conditions.append(
                    getattr(model, field).ilike(f'%{value}%')
                )
        if like_conditions:
            query = query.filter(or_(*like_conditions))
    return query


def get_by_sel(
    db: Session,
    model: Any,
    current_user_id: Optional[int] = None,
    filters: Optional[Dict[str, Any]] = None,
    join_type: Optional[str] = 'join',
):
    query = db.query(model)

    # Adicionando filtro especial para o modelo User
    if model.__name__ == 'User' and filters and 'current_user_id' in filters:
        current_user_id = filters['current_user_id']
        query = query.filter(
            or_(
                model.eh_deletado.is_(False),
                model.id == current_user_id,
            ),
        )

    query = handle_joins(query, model, filters, join_type)

    query = apply_filter_plus(query, model, filters)

    query = apply_like_filters(query, model, filters)
    return query


def check_related_models(
    db: Session,
    model: Any,
    model_id: int,
    current_user_id: int,
    related_models: List[Any],
):
    """
    Verifica se um modelo possui associação com outros modelos.
         Parâmetros:
             db: Session
             model: Any
             model_id: int
             current_user_id: int
             related_models: List[Any]
         Retorno:
             bool
    """
    filter_plus = {'id': model_id}

    if related_models is None:
        return False

    query = get_by_sel(
        db=db,
        model=model,
        current_user_id=current_user_id,
        filters={
            'joins': related_models,
            'filter_plus': filter_plus,
        },
        join_type='outerjoin',
    )

    result = query.first()
    if result is None:
        return False

    # Mapeamento das chaves de junção
    field_mapping = {
        'User': 'users_id',
        'Post': 'posts_id',
        'Message': 'messages_id',
        'Favorite': 'favorites_id',
        'Delivery': 'deliveries_id',
        'Event': 'events_id',
        'Watchlist': 'watchlists_id',
        'Calendar': 'calendars_id',
        'Category': 'categories_id',
        'Organization': 'organizations_id',
    }

    found_association = False

    for idx, related_model in enumerate(related_models):
        model_name = related_model.__name__
        related_field = field_mapping.get(model_name)

        if related_field is None:
            continue

        try:
            related_field_value = result[idx + 1]
            if related_field_value is not None:
                found_association = True
                break
        except IndexError:
            print(f'Índice {idx + 1} não encontrado no resultado.')

    return found_association
