import asyncio
import sys

from fast_rafa.core.database_seed import get_session
from fast_rafa.seeds import Seed


async def run_seed_all(session):
    result = await Seed.seed_all(session)
    print(result)


async def run_seed_categories(session):
    result = await Seed.seed_categories(session)
    print(result)


async def run_seed_events(session):
    result = await Seed.seed_events(session)
    print(result)


async def run_seed_organizations(session):
    result = await Seed.seed_organizations(session)
    print(result)


async def run_seed_users(session):
    result = await Seed.seed_users(session)
    print(result)


async def run_seed_posts(session):
    result = await Seed.seed_posts(session)
    print(result)


async def run_task_seed():
    """
    Interpreta argumentos passados após 'task seed'
    para rodar o seed específico.
    """
    args = sys.argv[1:]
    if len(args) < 1:  # Corrigido para checar se há pelo menos um argumento
        print('Uso: task seed <all|categories|events|users>')
        sys.exit(1)

    command = args[0]  # Corrigido para acessar args[0], não args[1]

    loop = asyncio.get_event_loop()
    session = await loop.run_in_executor(None, lambda: next(get_session()))

    if command == 'all':
        await run_seed_all(session)
    elif command == 'organizations':
        await run_seed_organizations(session)
    elif command == 'categories':
        await run_seed_categories(session)
    elif command == 'events':
        await run_seed_events(session)
    elif command == 'users':
        await run_seed_users(session)
    elif command == 'posts':
        await run_seed_posts(session)
    else:
        print(f'Comando inválido: {command}')
        print('Uso: task seed <all|categories|events|users>')
