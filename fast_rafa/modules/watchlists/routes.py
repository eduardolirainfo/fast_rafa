from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from fast_rafa.core.database import get_session
from fast_rafa.core.security import get_current_user
from fast_rafa.modules.users.models import User
from fast_rafa.modules.watchlists.models import Watchlist

router = APIRouter()


@router.post('/warning', status_code=HTTPStatus.OK)
def get_client_ip(
    ip: str,
    db: Session = Depends(get_session),
    current_user: Optional[User] = Depends(get_current_user),
):
    if not current_user:
        usuario = Watchlist(endereco_ip=ip, quantidade=1)
        db.add(usuario)
        db.commit()
        return {
            'aviso': 'Você está recebendo um aviso porque violou as regras '
            'da comunidade.'
        }
    else:
        usuario = Watchlist(id_usuario=current_user.id, quantidade=1)
        db.add(usuario)
        db.commit()
        return {
            'aviso': 'Você está recebendo um aviso porque violou as regras '
            'da comunidade.'
        }


@router.put('/repeat', status_code=HTTPStatus.OK)
def repeat_offense(
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    id_usuario = current_user.id
    usuario = (
        db.query(Watchlist).filter(Watchlist.id_usuario == id_usuario).first()
    )

    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado na lista de observação.',
        )

    usuario.quantidade = 2
    db.commit()
    return {
        'aviso': 'Você não tem mais avisos restantes. Se violar nossos '
        'padrões da comunidade, será banido do Mealize.'
    }


@router.put('/apologized', status_code=HTTPStatus.OK)
def apologized(id_usuario: int, db: Session = Depends(get_session)):
    usuario = (
        db.query(Watchlist).filter(Watchlist.id_usuario == id_usuario).first()
    )

    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado na lista de observação.',
        )

    usuario.quantidade = 1
    db.commit()
    return {
        'mensagem': 'Obrigado por fazer a coisa certa, nós apreciamos. '
        'Por favor, continue a ser bom com os outros.'
    }


@router.put('/blacklist', status_code=HTTPStatus.OK)
def add_to_blacklist(
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    id_usuario = current_user.id
    usuario = (
        db.query(Watchlist).filter(Watchlist.id_usuario == id_usuario).first()
    )

    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado na lista de observação.',
        )

    usuario.quantidade = 3
    db.commit()
    return {
        'mensagem': 'Você agora está banido do Mealize. Seja bom com os '
        'outros.'
    }


@router.post('/blacklist', status_code=HTTPStatus.OK)
def ban_user(ip: str, db: Session = Depends(get_session)):
    usuario = Watchlist(endereco_ip=ip, quantidade=3)
    db.add(usuario)
    db.commit()
    return {
        'mensagem': 'Você agora está banido do Fast RAFA. Seja bom com os '
        'outros.'
    }
