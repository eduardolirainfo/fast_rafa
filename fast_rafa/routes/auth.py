from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_rafa.database import get_session
from fast_rafa.models.user import User
from fast_rafa.schemas.auth import Auth
from fast_rafa.security import create_access_token, verify_password

router = APIRouter(prefix='/auth')  # Removido para evitar double prefix


@router.post(
    '/token', response_model=Auth
)  # Mudado para /token conforme padrão OAuth2
async def login_for_access_token(
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
