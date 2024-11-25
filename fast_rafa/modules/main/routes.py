from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from fast_rafa.core.database import Session, get_session
from fast_rafa.core.logger import setup_logger
from fast_rafa.core.security import get_user_from_cookie
from fast_rafa.modules.categories_main.services import get_categories
from fast_rafa.modules.events.services import get_suggested_events
from fast_rafa.modules.organizations.services import (
    get_list_organizations,
    get_suggested_organizations,
)
from fast_rafa.modules.posts.services import get_posts_by_organization
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
        user, error = await get_user_from_cookie(request, db)

        if not user:
            logger.warning(f'Logout attempted but {error}')
            return RedirectResponse(
                url='/auth/login', status_code=status.HTTP_302_FOUND
            )

        user.iniciais = iniciais(f'{user.primeiro_nome} {user.sobrenome}')
        user_with_org = user.get_user_with_organization
        if not user_with_org:
            return RedirectResponse(
                url='/auth/login', status_code=status.HTTP_302_FOUND
            )

        categorias = get_categories(db)

        if user.organization:
            posts_organizacoes = get_posts_by_organization(
                db, user.organization.id, user.organization.nao_governamental
            )
        else:
            posts_organizacoes = []

        suggested_orgs = get_suggested_organizations(db, user.id_organizacao)

        suggested_events = get_suggested_events(db, user.id_organizacao)

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
        },
    )


@router.get('/profile')
async def profile(request: Request, db: Session = Depends(get_session)):
    try:
        user, error = await get_user_from_cookie(request, db)

        if not user:
            logger.warning(f'Logout attempted but {error}')
            return RedirectResponse(
                url='/auth/login', status_code=status.HTTP_302_FOUND
            )
        user.iniciais = iniciais(f'{user.primeiro_nome} {user.sobrenome}')
        user_with_org = user.get_user_with_organization
        if not user_with_org:
            return RedirectResponse(
                url='/auth/login', status_code=status.HTTP_302_FOUND
            )

        categorias = get_categories(db)

        if user.organization:
            posts_organizacoes = get_posts_by_organization(
                db, user.organization.id, user.organization.nao_governamental
            )
        else:
            posts_organizacoes = []

        suggested_orgs = get_suggested_organizations(db, user.id_organizacao)

        suggested_events = get_suggested_events(db, user.id_organizacao)

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
        },
    )


@router.get('/edit-profile', response_class=HTMLResponse)
async def edit_profile(request: Request, db: Session = Depends(get_session)):
    try:
        # Tenta obter o usuário a partir do cookie
        user, error = await get_user_from_cookie(request, db)

        if not user:
            logger.warning(f'Efetuou logout, mas {error}')
            return RedirectResponse(url='/auth/login')

        user.iniciais = iniciais(f'{user.primeiro_nome} {user.sobrenome}')
        categorias = get_categories(db)
        posts_organizacoes = get_posts_by_organization(
            db, user.organization.id, user.organization.nao_governamental
        )
        suggested_orgs = get_suggested_organizations(db, user.id_organizacao)
        suggested_events = get_suggested_events(db, user.id_organizacao)
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
        },
    )
