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
            Post.quantidade > 0,
            Post.id_organizacao != user_organization_id,
        )
        .group_by(Organization.id)
        .order_by(func.count(Post.id).desc())
        .limit(5)
        .all()
    )


def get_organizations(db: Session):
    return db.query(Organization).all()


def get_list_organizations(db: Session):
    organizations = get_organizations(db)
    organizations_data = [
        {'id': org.id, 'display_name': org.display_name}
        for org in organizations
    ]
    return organizations_data
