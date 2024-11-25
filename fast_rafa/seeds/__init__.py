from .categories import seed_categories, undo_categories
from .categories_main import seed_categories_main, undo_categories_main
from .events import seed_events, undo_events
from .organizations import seed_organizations, undo_organizations
from .posts import seed_posts, undo_posts
from .users import seed_users, undo_users


class Seed:
    @staticmethod
    async def seed_categories_main(session):
        """Insere categorias principais."""
        await seed_categories_main(session)
        return 'Categorias principais incluídas com sucesso!'

    async def seed_categories(session):
        """Insere categorias iniciais."""
        await seed_categories(session)
        return 'Categorias incluídas com sucesso!'

    @staticmethod
    async def seed_organizations(session):
        """Insere organizações iniciais."""
        await seed_organizations(session)
        return 'Organizações incluídas com sucesso!'

    @staticmethod
    async def seed_users(session):
        """Insere usuários iniciais."""
        result = await seed_users(session)
        if result:
            return result

    @staticmethod
    async def seed_posts(session):
        """Insere posts iniciais."""
        result = await seed_posts(session)
        if result:
            return result

    @staticmethod
    async def seed_events(session):
        """Insere eventos iniciais."""
        result = await seed_events(session)
        if result:
            return result

    @staticmethod
    async def undo_categories(session):
        """Reverte categorias."""
        result = await undo_categories(session)
        if result:
            return result

    @staticmethod
    async def undo_categories_main(session):
        """Reverte categorias principais."""
        result = await undo_categories_main(session)
        if result:
            return result

    @staticmethod
    async def undo_organizations(session):
        """Reverte organizações."""
        result = await undo_organizations(session)
        if result:
            return result

    @staticmethod
    async def undo_users(session):
        """Reverte usuários."""
        result = await undo_users(session)
        if result:
            return result

    @staticmethod
    async def undo_posts(session):
        """Reverte posts."""
        result = await undo_posts(session)
        if result:
            return result

    @staticmethod
    async def undo_events(session):
        """Reverte eventos."""
        result = await undo_events(session)
        if result:
            return result

    @staticmethod
    async def seed_all(session):
        """Insere todos os dados iniciais."""
        await Seed.seed_categories_main(session)
        await Seed.seed_categories(session)
        await Seed.seed_organizations(session)
        await Seed.seed_users(session)
        await Seed.seed_posts(session)
        await Seed.seed_events(session)
        return 'Inclusão de dados iniciais realizada com sucesso!'

    @staticmethod
    async def undo_all(session):
        """Reverte todos os dados iniciais."""
        await Seed.undo_categories(session)
        await Seed.undo_categories_main(session)
        await Seed.undo_organizations(session)
        await Seed.undo_users(session)
        await Seed.undo_posts(session)
        await Seed.undo_events(session)
        return 'Limpeza de dados iniciais realizada com sucesso!'
