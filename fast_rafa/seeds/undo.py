import asyncio
import sys

from fast_rafa.core.database_seed import get_session
from fast_rafa.seeds import Seed


async def run_undo_all(session):
    result = await Seed.undo_all(session)
    print(result)


async def run_undo_categories_main(session):
    result = await Seed.undo_categories_main(session)
    print(result)


async def run_undo_categories(session):
    result = await Seed.undo_categories(session)
    print(result)


async def run_undo_events(session):
    result = await Seed.undo_events(session)
    print(result)


async def run_undo_organizations(session):
    result = await Seed.undo_organizations(session)
    print(result)


async def run_undo_users(session):
    result = await Seed.undo_users(session)
    print(result)


async def run_undo_posts(session):
    result = await Seed.undo_posts(session)
    print(result)


async def run_task_undo():
    """
    Interpreta argumentos passados após 'task undo'
    para rodar o undo específico.
    """
    args = sys.argv[1:]
    if len(args) < 1:  # Verifica se o argumento foi passado
        print('Uso: task undo <all|categories|events|users>')
        sys.exit(1)

    command = args[0]  # O comando 'undo'

    # Obtenha a sessão
    loop = asyncio.get_event_loop()
    session = await loop.run_in_executor(None, lambda: next(get_session()))

    # Execute o undo correto com base no comando
    if command == 'all':
        await run_undo_all(session)
    elif command == 'organizations':
        await run_undo_organizations(session)
    elif command == 'categories_main':
        await run_undo_categories_main(session)
    elif command == 'categories':
        await run_undo_categories(session)
    elif command == 'events':
        await run_undo_events(session)
    elif command == 'users':
        await run_undo_users(session)
    elif command == 'posts':
        await run_undo_posts(session)
    else:
        print(f'Comando inválido: {command}')
        print('Uso: task undo <all|categories|events|users>')
