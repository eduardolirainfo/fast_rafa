from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Optional, Tuple

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, encode
from jwt.exceptions import PyJWTError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session
from zoneinfo import ZoneInfo

from fast_rafa.core.database import get_session
from fast_rafa.modules.auth.schemas import TokenData
from fast_rafa.modules.users.models import User

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')

SECRET_KEY = 'secret'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class CustomOAuth2PasswordBearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        try:
            token = await super().__call__(request)
            print(f'Token recebido: {token}')  # Adicione este log
            return token
        except HTTPException as e:
            if e.status_code == status.HTTP_401_UNAUTHORIZED:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Você precisa estar autenticado'
                    ' para realizar esta operação',
                    headers={'WWW-Authenticate': 'Bearer'},
                )
            raise e


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data_payload: dict, expires_delta: Optional[timedelta] = None
) -> str:
    to_encode = data_payload.copy()

    if expires_delta:
        expire = datetime.now(tz=ZoneInfo('UTC')) + expires_delta
    else:
        expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    db: Session = Depends(get_session),
    token: str = Depends(CustomOAuth2PasswordBearer(tokenUrl='auth/token')),
) -> User:
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Credenciais inválidas',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f'Payload do Token: {payload}')
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except PyJWTError:
        raise credentials_exception

    user = db.scalar(select(User).where(User.username == token_data.username))
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.eh_deletado:
        raise HTTPException(status_code=400, detail='Usuário Inativo')
    return current_user


async def get_user_from_cookie(
    request: Request, db: Session
) -> Tuple[Optional[User], Optional[str]]:
    """
    Tenta obter o usuário atual a partir do token no cookie.
    Retorna uma tupla com (usuário, mensagem_erro).
    Se não encontrar usuário, retorna (None, mensagem_erro).
    """
    try:
        token = request.cookies.get('access_token')
        if not token:
            return None, 'Token não encontrado no cookie'

        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')

        if not username:
            return None, 'Username não encontrado no token'

        user = db.scalar(select(User).where(User.username == username))
        if not user:
            return None, 'Usuário não encontrado'

        return user, None

    except PyJWTError:
        return None, 'Token inválido'
    except Exception as e:
        return None, f'Erro ao processar token: {str(e)}'


async def get_user_and_access_token_from_cookie(
    request: Request, db: Session
) -> Tuple[Optional[User], Optional[str], Optional[str]]:
    """
    Tenta obter o usuário atual e o access_token a partir do token no cookie.
    Retorna uma tupla com (usuário, access_token, mensagem_erro).
    Se não encontrar usuário ou access_token,
    retorna (None, None, mensagem_erro).
    """
    try:
        token = request.cookies.get('access_token')
        if not token:
            return None, None, 'Token não encontrado no cookie'

        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')

        if not username:
            return None, None, 'Username não encontrado no token'

        user = db.scalar(select(User).where(User.username == username))
        if not user:
            return None, None, 'Usuário não encontrado'

        return user, token, None

    except PyJWTError:
        return None, None, 'Token inválido'
    except Exception as e:
        return None, None, f'Erro ao processar token: {str(e)}'
