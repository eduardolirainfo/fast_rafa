from .categories import seed_categories, undo_categories
from .events import seed_events, undo_events
from .organizations import seed_organizations, undo_organizations
from .posts import seed_posts, undo_posts
from .users import seed_users, undo_users


class Seed:
    @staticmethod
    def seed_categories(session):
        """Insere categorias iniciais."""
        seed_categories(session)
        return 'Categorias incluídas com sucesso!'

    @staticmethod
    def seed_organizations(session):
        """Insere organizações iniciais."""
        seed_organizations(session)
        return 'Organizações incluídas com sucesso!'

    @staticmethod
    def seed_users(session):
        """Insere usuários iniciais."""
        seed_users(session)
        return 'Usuários incluídos com sucesso!'

    @staticmethod
    def seed_posts(session):
        """Insere posts iniciais."""
        seed_posts(session)
        return 'Posts incluídos com sucesso!'

    @staticmethod
    def seed_events(session):
        """Insere eventos iniciais."""
        seed_events(session)
        return 'Eventos incluídos com sucesso!'

    @staticmethod
    def undo_categories(session):
        """Reverte categorias."""
        undo_categories(session)
        return 'Limpeza das categorias realizada com sucesso!'

    @staticmethod
    def undo_organizations(session):
        """Reverte organizações."""
        undo_organizations(session)
        return 'Limpeza das organizações realizada com sucesso!'

    @staticmethod
    def undo_users(session):
        """Reverte usuários."""
        undo_users(session)
        return 'Limpeza dos usuários realizada com sucesso!'

    @staticmethod
    def undo_posts(session):
        """Reverte posts."""
        undo_posts(session)
        return 'Limpeza dos posts realizada com sucesso!'

    @staticmethod
    def undo_events(session):
        """Reverte eventos."""
        undo_events(session)
        return 'Limpeza dos eventos realizada com sucesso!'

    @staticmethod
    def seed_all(session):
        """Insere todos os dados iniciais."""
        Seed.seed_categories(session)
        Seed.seed_organizations(session)
        Seed.seed_users(session)
        Seed.seed_posts(session)
        Seed.seed_events(session)
        return 'Inclusão de dados iniciais realizada com sucesso!'

    @staticmethod
    def undo_all(session):
        """Reverte todos os dados iniciais."""
        Seed.undo_categories(session)
        Seed.undo_organizations(session)
        Seed.undo_users(session)
        Seed.undo_posts(session)
        Seed.undo_events(session)
        return 'Limpeza de dados iniciais realizada com sucesso!'
