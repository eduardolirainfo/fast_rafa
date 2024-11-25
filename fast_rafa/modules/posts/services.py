from sqlalchemy.orm import Session, joinedload

from fast_rafa.modules.categories.models import Category
from fast_rafa.modules.organizations.models import Organization
from fast_rafa.modules.posts.models import Post


def get_posts_by_organization(
    db: Session, user_organization_id: int, is_ngo: bool
):
    query = db.query(Post).join(Organization).join(Category)

    if is_ngo:
        query = query.filter(
            Organization.nao_governamental == True,
            user_organization_id != Organization.id,
        )
    else:
        query = query.filter(
            Organization.nao_governamental == False,
            user_organization_id != Organization.id,
        )

    return (
        query.options(
            joinedload(Post.organizations),
            joinedload(Post.categories),
            joinedload(Post.uploader),
        )
        .offset(0)
        .limit(5)
        .all()
    )
