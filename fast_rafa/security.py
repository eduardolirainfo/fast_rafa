from pwdlib import PasswordHash
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fast_rafa.database import get_session

pwd_context = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_current_user(
    db: Session = Depends(get_session)
):
    pass
