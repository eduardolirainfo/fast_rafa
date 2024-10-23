from .categories import seed_categories, undo_categories

# from .organizations import seed_organizations, undo_organizations
# from .users import seed_users, undo_users
# from .posts import seed_posts, undo_posts


def seed_all():
    """ Envie todos os dados iniciais."""
    seed_categories()
    # seed_organizations()
    # seed_users()
    # seed_posts()
    print("Inclusão de dados iniciais realizada com sucesso!")


def undo_all():
    """Reverte todos os dados iniciais."""
    undo_categories()
    # undo_organizations()
    # undo_users()
    # undo_posts()
    print("Limpeza de dados iniciais realizada com sucesso!")
