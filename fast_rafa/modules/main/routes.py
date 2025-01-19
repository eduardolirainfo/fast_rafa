from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from datetime import datetime
from fast_rafa.core.database import Session, get_session
from fast_rafa.core.logger import setup_logger
from fast_rafa.core.security import (
    get_user_and_access_token_from_cookie,
)
from fast_rafa.modules.categories_main.services import get_categories
from fast_rafa.modules.events.services import get_suggested_events, get_events
from fast_rafa.modules.organizations.services import (
    get_list_organizations,
    get_organizations,
    get_suggested_organizations,
)
from fast_rafa.modules.posts.services import (
    get_posts_by_category_main,
    get_posts_by_id,
    get_posts_by_organization,
    get_posts_by_user,
)
from fast_rafa.utils.funcs import iniciais

templates = Jinja2Templates(directory='fast_rafa/templates')
logger = setup_logger()

router = APIRouter()


@router.get('/')
async def index(request: Request):
    return RedirectResponse(url='/home')


@router.get('/home')
async def home(request: Request, db: Session = Depends(get_session)):
    try:
        (
            user,
            categorias,
            posts_organizacoes,
            suggested_orgs,
            suggested_events,
            access_token,
            error,
        ) = await get_common_data(request, db)

        if not user:
            logger.warning(f'Logout attempted but {error}')
            return RedirectResponse(
                url='/auth/login', status_code=status.HTTP_302_FOUND
            )

        user_with_org = user.get_user_with_organization
        if not user_with_org:
            return RedirectResponse(
                url='/auth/login', status_code=status.HTTP_302_FOUND
            )

    except Exception as e:
        logger.error(f'Erro ao obter usuário: {e}')
        return RedirectResponse(url='/auth/login')

    return templates.TemplateResponse(
        'home.html',
        {
            'request': request,
            'current_user': user,
            'categories': categorias,
            'posts': posts_organizacoes,
            'suggested_orgs': suggested_orgs,
            'suggested_events': suggested_events,
            'access_token': access_token,
        },
    )


@router.get('/profile')
async def profile(request: Request, db: Session = Depends(get_session)):
    try:
        (
            user,
            categorias,
            posts_organizacoes,
            suggested_orgs,
            suggested_events,
            access_token,
            error,
        ) = await get_common_data(request, db)

        if not user:
            logger.warning(f'Logout attempted but {error}')
            return RedirectResponse(
                url='/auth/login', status_code=status.HTTP_302_FOUND
            )

        user_with_org = user.get_user_with_organization
        if not user_with_org:
            return RedirectResponse(
                url='/auth/login', status_code=status.HTTP_302_FOUND
            )

    except Exception as e:
        logger.error(f'Erro ao obter usuário: {e}')
        return RedirectResponse(url='/auth/login')

    return templates.TemplateResponse(
        'profile.html',
        {
            'request': request,
            'current_user': user,
            'categories': categorias,
            'posts': posts_organizacoes,
            'suggested_orgs': suggested_orgs,
            'suggested_events': suggested_events,
            'access_token': access_token,
        },
    )


@router.get('/edit-profile', response_class=HTMLResponse)
async def edit_profile(request: Request, db: Session = Depends(get_session)):
    try:
        (
            user,
            categorias,
            posts_organizacoes,
            suggested_orgs,
            suggested_events,
            access_token,
            error,
        ) = await get_common_data(request, db)

        if not user:
            logger.warning(f'Logout attempted but {error}')
            return RedirectResponse(
                url='/auth/login', status_code=status.HTTP_302_FOUND
            )
        organizations_data = get_list_organizations(db)
    except Exception as e:
        # Caso ocorra algum erro, registra o erro e redireciona para o perfil
        logger.error(f'Erro ao carregar a página de edição de perfil: {e}')
        return RedirectResponse(url='/profile')

    return templates.TemplateResponse(
        'editers/edit_profile.html',
        {
            'request': request,
            'current_user': user,
            'categories': categorias,
            'posts': posts_organizacoes,
            'suggested_orgs': suggested_orgs,
            'suggested_events': suggested_events,
            'organizations': organizations_data,
            'access_token': access_token,
        },
    )


@router.get('/posts')
async def user_posts(request: Request, db: Session = Depends(get_session)):
    language = request.headers.get('Accept-Language', 'pt').split(',')[0]

    try:
        (
            user,
            categorias,
            _,
            suggested_orgs,
            suggested_events,
            access_token,
            error,
        ) = await get_common_data(request, db)

        print(user)
        if not user:
            logger.warning(f'Logout attempted but {error}')
            return RedirectResponse(
                url='/auth/login', status_code=status.HTTP_302_FOUND
            )
        user_id = user.id
        posts = get_posts_by_user(db, user_id, language)
        if not posts:
            posts = []

    except Exception as e:
        logger.error(f'Erro ao obter usuário: {e}')
        return RedirectResponse(url='/auth/login')

    return templates.TemplateResponse(
        'posts.html',
        {
            'request': request,
            'current_user': user,
            'categories': categorias,
            'posts': posts,
            'suggested_orgs': suggested_orgs,
            'suggested_events': suggested_events,
            'access_token': access_token,
        },
    )


@router.get('/posts/{post_id}', response_class=HTMLResponse)
async def post_detail(
    request: Request, post_id: int, db: Session = Depends(get_session)
):
    language = request.headers.get('Accept-Language', 'pt').split(',')[0]

    try:
        (
            user,
            categorias,
            _,
            suggested_orgs,
            suggested_events,
            access_token,
            error,
        ) = await get_common_data(request, db)

        if not user:
            logger.warning(f'Logout attempted but {error}')
            return RedirectResponse(
                url='/auth/login', status_code=status.HTTP_302_FOUND
            )

        post = get_posts_by_id(db, post_id, user.id, language)

        if not post:
            return RedirectResponse(url='/home')

    except Exception as e:
        logger.error(f'Erro ao obter post: {e}')
        return RedirectResponse(url='/home')

    return templates.TemplateResponse(
        'post.html',
        {
            'request': request,
            'current_user': user,
            'categories': categorias,
            'post': post,
            'suggested_orgs': suggested_orgs,
            'suggested_events': suggested_events,
            'access_token': access_token,
        },
    )


@router.get('/categories/{category_slug}', response_class=HTMLResponse)
async def category_posts(
    request: Request,
    category_slug: str,
    db: Session = Depends(get_session),
    offset: int = 0,
    limit: int = 5,
):
    language = request.headers.get('Accept-Language', 'pt').split(',')[0]
    try:
        (
            user,
            categorias,
            _,
            suggested_orgs,
            suggested_events,
            access_token,
            error,
        ) = await get_common_data(request, db)

        if not user:
            logger.warning(f'Logout attempted but {error}')
            return RedirectResponse(
                url='/auth/login', status_code=status.HTTP_302_FOUND
            )

        posts = get_posts_by_category_main(
            db, category_slug, language, offset, limit
        )

    except Exception as e:
        logger.error(f'Erro ao obter posts por categoria: {e}')
        return RedirectResponse(url='/home')

    return templates.TemplateResponse(
        'posts.html',
        {
            'request': request,
            'current_user': user,
            'categories': categorias,
            'posts': posts,
            'suggested_orgs': suggested_orgs,
            'suggested_events': suggested_events,
            'access_token': access_token,
        },
    )

    return category_posts


@router.get('/organizations/', response_class=HTMLResponse)
async def organizations_list(
    request: Request,
    organization_id: int = None,
    db: Session = Depends(get_session),
):
    try:
        (
            user,
            categorias,
            _,
            suggested_orgs,
            suggested_events,
            access_token,
            error,
        ) = await get_common_data(request, db)

        if not user:
            logger.warning(f'Logout attempted but {error}')
            return RedirectResponse(
                url='/auth/login', status_code=status.HTTP_302_FOUND
            )

        organizations = get_organizations(
            db, None, user.id_organizacao, user.eh_gerente
        )
    except Exception as e:
        logger.error(f'Erro ao obter organizações: {e}')
        return RedirectResponse(url='/home')

    return templates.TemplateResponse(
        'organizations.html',
        {
            'request': request,
            'current_user': user,
            'categories': categorias,
            'organizations': organizations,
            'suggested_orgs': suggested_orgs,
            'suggested_events': suggested_events,
            'access_token': access_token,
        },
    )


@router.get('/organizations/{organization_id}', response_class=HTMLResponse)
async def organizations_detail(
    request: Request, organization_id: int, db: Session = Depends(get_session)
):
    try:
        (
            user,
            categorias,
            _,
            suggested_orgs,
            suggested_events,
            access_token,
            error,
        ) = await get_common_data(request, db)

        if not user:
            logger.warning(f'Logout attempted but {error}')
            return RedirectResponse(
                url='/auth/login', status_code=status.HTTP_302_FOUND
            )

        organizations = get_organizations(
            db, organization_id, user.id_organizacao, user.eh_gerente
        )

        if not organizations:
            raise ValueError('Organização não encontrada')
    except Exception as e:
        logger.error(f'Erro ao obter posts por organização detalhada: {e}')
        return RedirectResponse(url='/home')

    return templates.TemplateResponse(
        'organizations.html',
        {
            'request': request,
            'current_user': user,
            'categories': categorias,
            'organizations': organizations,
            'suggested_orgs': suggested_orgs,
            'suggested_events': suggested_events,
            'access_token': access_token,
        },
    )


@router.get(
    '/organizations/{organization_id}/stats/', response_class=HTMLResponse
)
async def organization_stats(
    request: Request, organization_id: int, db: Session = Depends(get_session)
):
    try:
        (
            user,
            categorias,
            _,
            suggested_orgs,
            suggested_events,
            access_token,
            error,
        ) = await get_common_data(request, db)

        if not user:
            logger.warning(f'Logout attempted but {error}')
            return RedirectResponse(
                url='/auth/login', status_code=status.HTTP_302_FOUND
            )

        organizations = get_organizations(
            db, organization_id, user.id_organizacao, user.eh_gerente
        )

        if not organizations:
            raise ValueError('Organização não encontrada')

        categorias_list = [cat.categoria for cat in categorias]
        doacoes_por_mes = [
            50,
            60,
            75,
            80,
            90,
            110,
            120,
            140,
            150,
            160,
            170,
            180,
        ]
        doacoes_por_categoria = [100, 200, 150, 80, 120]
        doacoes_ao_longo_do_tempo = [
            5,
            10,
            15,
            20,
            25,
            30,
            35,
            40,
            45,
            50,
            55,
            60,
        ]
        comida_nao_desperdicada = [
            10,
            20,
            30,
            40,
            50,
            60,
            70,
            80,
            90,
            100,
            110,
            120,
        ]

    except Exception as e:
        logger.error(f'Erro ao obter posts por organização: {e}')

    return templates.TemplateResponse(
        'stats.html',
        {
            'request': request,
            'current_user': user,
            'categories': categorias,
            'categories_list': categorias_list,
            'organizations': organizations,
            'suggested_orgs': suggested_orgs,
            'suggested_events': suggested_events,
            'access_token': access_token,
            'doacoes_por_mes': doacoes_por_mes,
            'doacoes_por_categoria': doacoes_por_categoria,
            'doacoes_ao_longo_do_tempo': doacoes_ao_longo_do_tempo,
            'comida_nao_desperdicada': comida_nao_desperdicada,
        },
    )


@router.get('/events', response_class=HTMLResponse)
async def events_list(request: Request, db: Session = Depends(get_session)):
    try:
        (
            user,
            categorias,
            _,
            suggested_orgs,
            suggested_events,
            access_token,
            error,
        ) = await get_common_data(request, db)

        if not user:
            logger.warning(f'Logout attempted but {error}')
            return RedirectResponse(
                url='/auth/login', status_code=status.HTTP_302_FOUND
            )

        events = get_events(db, None, user.id_organizacao, user.eh_gerente)
        current_time = datetime.now()

        for event in events:
            # Ajustar a data de encerramento se necessário
            if event.data < event.fechado:
                event.fechado = event.data

            if event.fechado < event.data and event.data > current_time:
                event.fechado = event.data

            dias_restantes = (event.fechado - current_time).days

            # Verificar se o evento está ativo ou encerrado
            if event.fechado > current_time:
                event.status = 'ativo'
            else:
                event.status = 'encerrado'

            # Adicionar o campo de dias restantes no evento
            event.dias_restantes = dias_restantes

    except Exception as e:
        logger.error(f'Erro ao obter eventos: {e}')
        return RedirectResponse(url='/home')

    return templates.TemplateResponse(
        'events.html',
        {
            'request': request,
            'current_user': user,
            'categories': categorias,
            'suggested_orgs': suggested_orgs,
            'suggested_events': suggested_events,
            'access_token': access_token,
            'events': events,
            'current_time': current_time,
        },
    )


@router.get('/events/{event_slug}', response_class=HTMLResponse)
async def event_detail(
    request: Request, event_slug: str, db: Session = Depends(get_session)
):
    try:
        (
            user,
            categorias,
            _,
            suggested_orgs,
            suggested_events,
            access_token,
            error,
        ) = await get_common_data(request, db)

        if not user:
            logger.warning(f'Logout attempted but {error}')
            return RedirectResponse(
                url='/auth/login', status_code=status.HTTP_302_FOUND
            )

        events = get_events(
            db, event_slug, user.id_organizacao, user.eh_gerente
        )

    except Exception as e:
        logger.error(f'Erro ao obter eventos: {e}')
        return RedirectResponse(url='/home')

    return templates.TemplateResponse(
        'event.html',
        {
            'request': request,
            'current_user': user,
            'categories': categorias,
            'suggested_orgs': suggested_orgs,
            'suggested_events': suggested_events,
            'access_token': access_token,
            'events': events,
        },
    )


@router.get('/search', response_class=HTMLResponse)
async def search(
    request: Request, query: str = '', db: Session = Depends(get_session)
):
    try:
        (
            user,
            categorias,
            _,
            suggested_orgs,
            suggested_events,
            access_token,
            error,
        ) = await get_common_data(request, db)

        if not user:
            logger.warning(f'Logout attempted but {error}')
            return RedirectResponse(
                url='/auth/login', status_code=status.HTTP_302_FOUND
            )

        posts = get_posts_by_category_main(db, query)
    except Exception as e:
        logger.error(f'Erro ao obter posts por pesquisa: {e}')
        return RedirectResponse(url='/home')

    return templates.TemplateResponse(
        'search_results.html',
        {
            'request': request,
            'current_user': user,
            'categories': categorias,
            'posts': posts,
            'suggested_orgs': suggested_orgs,
            'suggested_events': suggested_events,
            'access_token': access_token,
        },
    )


async def get_common_data(request: Request, db: Session):
    """
    Função para obter dados comuns que são usados nas rotas.
    Retorna também o erro caso o usuário não seja encontrado.
    """
    language = request.headers.get('Accept-Language', 'pt').split(',')[0]
    try:
        # Obter usuário e token de acesso
        (
            user,
            access_token,
            error,
        ) = await get_user_and_access_token_from_cookie(request, db)
        if not user:
            return (
                None,
                None,
                None,
                None,
                None,
                None,
                error,
            )  # Retorna o erro quando o usuário não é encontrado

        # Processar iniciais
        user.iniciais = iniciais(f'{user.primeiro_nome} {user.sobrenome}')
        organization = get_organizations(
            db, user.id_organizacao, user.id_organizacao, user.eh_gerente
        )
        if organization:
            user.quantidade_doacoes = organization.quantidade_doacoes

        # Obter categorias
        categorias = get_categories(db)

        # Obter posts da organização do usuário
        posts_organizacoes = []
        if user.organization:
            posts_organizacoes = get_posts_by_organization(
                db,
                user.organization.id,
                user.id,
                language,
            )

        # Obter organizações e eventos sugeridos
        suggested_orgs = get_suggested_organizations(db, user.id_organizacao)
        suggested_events = get_suggested_events(db, user.id_organizacao)
        return (
            user,
            categorias,
            posts_organizacoes,
            suggested_orgs,
            suggested_events,
            access_token,
            None,
        )  # Retorna None para o erro quando tudo está correto

    except Exception as e:
        logger.error(f'Erro ao obter dados comuns: {e}')
        return (
            None,
            None,
            None,
            None,
            None,
            None,
            str(e),
        )
