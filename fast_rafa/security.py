from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from fast_rafa.database import get_session
from fast_rafa.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)
) -> User:
    user = db.query(User).filter(User.senha_hash == token).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Usuário não autorizado.',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return user
