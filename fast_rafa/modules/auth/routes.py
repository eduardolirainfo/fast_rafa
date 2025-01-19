from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    Response,
    status,
)
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session
from zoneinfo import ZoneInfo

from fast_rafa.core.database import get_session
from fast_rafa.core.logger import setup_logger
from fast_rafa.core.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_user_from_cookie,
    verify_password,
)
from fast_rafa.modules.auth.schemas import Auth
from fast_rafa.modules.organizations.models import Organization
from fast_rafa.modules.users.models import User

router = APIRouter(prefix='/auth')
logger = setup_logger()


templates = Jinja2Templates(directory='fast_rafa/templates')


class LoginForm:
    def __init__(self, request: Request):
        self.request = (
            request  # Atribuir o objeto Request ao atributo self.request
        )
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def create_oauth_form(self):
        form = await self.request.form()
        self.username = form.get('username')
        self.password = form.get('password')


class RegisterForm:
    def __init__(self, request: Request):
        self.request = (
            request  # Atribuir o objeto Request ao atributo self.request
        )
        self.username: Optional[str] = None
        self.email: Optional[str] = None
        self.password: Optional[str] = None
        self.confirm_password: Optional[str] = None

    async def create_register_form(self):
        form = await self.request.form()
        self.username = form.get('username')
        self.email = form.get('email')
        self.password = form.get('password')
        self.confirm_password = form.get('confirm_password')


@router.post('/token', response_model=Auth)
async def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session),
):
    user = db.scalar(select(User).where(User.username == form_data.username))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,  # Mudado para 401
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    if not verify_password(form_data.password, user.senha_hash):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,  # Mudado para 401
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    access_token = create_access_token(data_payload={'sub': user.username})

    return Auth(access_token=access_token, token_type='bearer')


@router.get('/login', response_class=HTMLResponse)
async def authentication_page(request: Request):
    return templates.TemplateResponse(
        'login.html',
        {'request': request, 'current_user': None},
    )


@router.post('/login', response_class=JSONResponse)
async def login(request: Request, db: Session = Depends(get_session)):
    try:
        form = LoginForm(request)
        await form.create_oauth_form()

        user = db.scalar(select(User).where(User.username == form.username))
        if not user or not verify_password(form.password, user.senha_hash):
            message = 'Usuário ou senha inválidos'
            return JSONResponse(content={'message': message}, status_code=401)

        access_token = create_access_token(data_payload={'sub': user.username})

        response = JSONResponse(
            content={
                'message': 'Login bem-sucedido',
                'access_token': access_token,
            },
            status_code=200,
        )

        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=True,
            expires=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

        return response

    except HTTPException:
        message = 'Erro desconhecido'
        return JSONResponse(content={'message': message}, status_code=500)


@router.get('/logout')
async def logout(
    request: Request,
    db: Session = Depends(get_session),
):
    try:
        # Tenta obter o usuário atual antes de fazer logout
        user, error = await get_user_from_cookie(request, db)

        if user:
            logger.info(
                f'User logout successful - Username: {user.username}, '
                f'ID: {user.id}, Timestamp: {datetime.now(tz=ZoneInfo("UTC"))}'
            )
        else:
            logger.warning(f'Logout attempted but {error}')

        # Criar a resposta de redirecionamento
        response = RedirectResponse(
            url='/auth/login', status_code=status.HTTP_302_FOUND
        )

        # Deletar o cookie 'access_token' no logout
        response.delete_cookie(key='access_token', path='/')

        # Commit no banco de dados, caso necessário
        db.commit()

        return response

    except Exception as e:
        # Logar erro inesperado
        logger.error(f'Erro inesperado ao tentar deslogar: {str(e)}')
        response = RedirectResponse(
            url='/auth/login', status_code=status.HTTP_302_FOUND
        )
        return response


@router.get('/register', response_class=HTMLResponse)
async def register_page(request: Request, db: Session = Depends(get_session)):
    organizations = db.query(Organization).all()

    if not organizations:
        return RedirectResponse(
            url='/auth/login', status_code=status.HTTP_302_FOUND
        )

    organizations_data = [
        {'id': org.id, 'display_name': org.display_name}
        for org in organizations
    ]
    hoje = datetime.today()

    # Calculando a data máxima (18 anos atrás)
    data_maxima = (hoje - timedelta(days=365 * 18)).strftime('%Y-%m-%d')

    return templates.TemplateResponse(
        'register/users_form.html',
        {
            'request': request,
            'organizations': organizations_data,
            'current_user': None,
            'data_maxima': data_maxima,
        },
    )


def get_user_exception():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Não foi possível validar as credenciais',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    return credentials_exception


def token_exception():
    token_exception_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Usuário ou senha inválidos',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    return token_exception_response
