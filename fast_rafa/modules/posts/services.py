from sqlalchemy import func
from sqlalchemy.orm import Query, Session, joinedload

from fast_rafa.modules.categories.models import Category
from fast_rafa.modules.categories_main.models import CategoryMain
from fast_rafa.modules.favorites.models import Favorite
from fast_rafa.modules.organizations.models import Organization
from fast_rafa.modules.posts.models import Post
from fast_rafa.utils.funcs import formatar_data


def add_likes_count(query: Query, db: Session) -> Query:
    """Adiciona uma subquery para contar likes de cada post"""
    likes_subquery = (
        db.query(func.count(Favorite.id))
        .filter(Favorite.id_postagem == Post.id)
        .correlate(Post)
        .scalar_subquery()
        .label('total_likes')
    )

    return query.add_columns(likes_subquery)


def get_posts_by_organization(
    db: Session,
    user_organization_id: int,
    user_id: int,
    is_ngo: bool,
    language: str = 'pt-BR',
):
    query = db.query(Post).join(Organization).join(Category)
    if is_ngo:
        governamental = True
        query = query.filter(
            Organization.nao_governamental == governamental,
            user_organization_id != Organization.id,
        )
    else:
        nao_governamental = False
        query = query.filter(
            Organization.nao_governamental == nao_governamental,
            user_organization_id != Organization.id,
        )

    posts_with_likes = []

    posts = (
        query.options(
            joinedload(Post.organizations),
            joinedload(Post.categories),
            joinedload(Post.uploader),
        )
        .offset(0)
        .limit(5)
        .all()
    )

    favoritos = (
        db.query(Favorite.id_postagem)
        .filter(Favorite.id_usuario == user_id)
        .all()
    )

    favoritos_set = {fav.id_postagem for fav in favoritos}

    for post in posts:
        total_likes = (
            db.query(Favorite).filter(Favorite.id_postagem == post.id).count()
        )
        eh_favorito = 1 if post.id in favoritos_set else 0
        post.criado_em_formatada = formatar_data(post.criado_em, language)
        post.total_likes = total_likes
        post.eh_favorito = eh_favorito

        posts_with_likes.append(post)

    return posts_with_likes


def get_posts_by_id(
    db: Session, post_id: int, user_id: int, language: str = 'pt-BR'
):
    query = db.query(Post).filter(Post.id == post_id)

    post = query.options(
        joinedload(Post.organizations),
        joinedload(Post.categories),
        joinedload(Post.uploader),
    ).first()

    favoritos = (
        db.query(Favorite)
        .filter(
            Favorite.id_usuario == user_id, Favorite.id_postagem == post_id
        )
        .all()
    )

    favoritos_set = {fav.id_postagem for fav in favoritos}

    if post:
        total_likes = (
            db.query(Favorite).filter(Favorite.id_postagem == post.id).count()
        )
        post.criado_em_formatada = formatar_data(post.criado_em, language)
        eh_favorito = 1 if post.id in favoritos_set else 0
        post.total_likes = total_likes
        post.eh_favorito = eh_favorito
    return post


def get_posts_by_category_main(
    db: Session,
    category_slug: str,
    language: str = 'pt-BR',
    offset: int = 0,
    limit: int = 5,
):
    category_main = (
        db.query(CategoryMain)
        .filter(CategoryMain.slug == category_slug)
        .first()
    )
    if not category_main:
        return []

    categories = (
        db.query(Category).filter(Category.id == category_main.id).all()
    )
    category_ids = [category.id for category in categories]

    query = db.query(Post).filter(Post.id_categoria.in_(category_ids))
    query = add_likes_count(query, db)
    posts = (
        query.options(
            joinedload(Post.organizations),
            joinedload(Post.categories),
            joinedload(Post.uploader),
        )
        .order_by(Post.criado_em.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    if posts:
        for post, total_likes in posts:
            post.criado_em_formatada = formatar_data(post.criado_em, language)
            post.total_likes = total_likes

    return [post for post, _ in posts]


def get_posts_by_user(db: Session, user_id: int, language: str = 'pt-BR'):
    query = db.query(Post).filter(Post.id_usuario == user_id)
    query = add_likes_count(query, db)

    posts = (
        query.options(
            joinedload(Post.organizations),
            joinedload(Post.categories),
            joinedload(Post.uploader),
            joinedload(Post.favorites),
        )
        .offset(0)
        .limit(5)
        .all()
    )

    if posts:
        for post, total_likes in posts:
            post.criado_em_formatada = formatar_data(post.criado_em, language)
            post.total_likes = total_likes

    return [post for post, _ in posts]


def get_posts_favorite_by_user(
    db: Session, user_id: int, language: str = 'pt-BR'
):
    query = (
        db.query(Post).join(Favorite).filter(Favorite.id_usuario == user_id)
    )

    query = add_likes_count(query, db)

    posts = (
        query.options(
            joinedload(Post.organizations),
            joinedload(Post.categories),
            joinedload(Post.uploader),
            joinedload(Post.favorites),
        )
        .offset(0)
        .limit(5)
        .all()
    )

    if posts:
        for post, total_likes in posts:
            post.criado_em_formatada = formatar_data(post.criado_em, language)
            post.total_likes = total_likes

    return [post for post, _ in posts]
