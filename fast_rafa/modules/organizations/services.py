from sqlalchemy import func
from sqlalchemy.orm import Session

from fast_rafa.modules.organizations.models import Organization
from fast_rafa.modules.posts.models import Post


def get_suggested_organizations(db: Session, user_organization_id: int):
    return (
        db.query(Organization, func.count(Post.id).label('post_count'))
        .join(Post, Post.id_organizacao == Organization.id)
        .filter(
            Post.status == 1,
            Post.data_validade >= func.now(),
            Post.quantidade != '',
            Post.id_organizacao != user_organization_id,
        )
        .group_by(Organization.id)
        .order_by(func.count(Post.id).desc())
        .limit(5)
        .all()
    )


def get_organizations(
    db: Session,
    organization_id: int = None,
    user_organization_id: int = None,
    user_eh_gerente: bool = None,
):
    query = db.query(Organization)
    gerente = False
    if user_eh_gerente is not None:
        gerente = user_eh_gerente

    if organization_id:
        query = query.filter(Organization.id == organization_id)
        organization = query.first()

        if organization:
            post_count = (
                db.query(func.count(Post.id))
                .filter(Post.id_organizacao == organization.id)
                .scalar()
            )
            organization.pode_editar = (
                organization.id == user_organization_id
            ) and gerente
            organization.quantidade_doacoes = (
                post_count or 0
            )  # Adicionando a quantidade de doações/postagens
            return organization
        else:
            return None

    else:
        organizations = query.all()

        result = []
        for organization in organizations:
            # Contagem de posts para cada organização
            post_count = (
                db.query(func.count(Post.id))
                .filter(Post.id_organizacao == organization.id)
                .scalar()
            )
            organization.pode_editar = (
                organization.id == user_organization_id
            ) and gerente
            organization.quantidade_doacoes = (
                post_count or 0
            )  # Definindo a quantidade de doações/postagens
            result.append(organization)

        return result


def get_list_organizations(db: Session):
    organizations = get_organizations(db)
    organizations_data = [
        {'id': org.id, 'display_name': org.display_name}
        for org in organizations
    ]
    return organizations_data
