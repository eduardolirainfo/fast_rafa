from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fast_rafa.core.database import get_session
from fast_rafa.seeds import Seed

router = APIRouter()


@router.post('/categories')
def run_seed_categories(db: Session = Depends(get_session)):
    Seed.seed_categories(db)
    return {'message': 'Categorias inseridas com sucesso!'}


@router.post('/organizations')
def run_seed_organizations(db: Session = Depends(get_session)):
    Seed.seed_organizations(db)
    return {'message': 'Organizações inseridas com sucesso!'}


@router.post('/users')
def run_seed_users(db: Session = Depends(get_session)):
    Seed.seed_users(db)
    return {'message': 'Usuários inseridos com sucesso!'}


@router.post('/posts')
def run_seed_posts(db: Session = Depends(get_session)):
    Seed.seed_posts(db)
    return {'message': 'Posts inseridos com sucesso!'}


@router.post('/events')
def run_seed_events(db: Session = Depends(get_session)):
    Seed.seed_events(db)
    return {'message': 'Eventos inseridos com sucesso!'}


@router.post('/undo/categories')
def undo_categories(db: Session = Depends(get_session)):
    Seed.undo_categories(db)
    return {'message': 'Limpeza das categorias realizada com sucesso!'}


@router.post('/undo/organizations')
def undo_organizations(db: Session = Depends(get_session)):
    Seed.undo_organizations(db)
    return {'message': 'Limpeza das organizações realizada com sucesso!'}


@router.post('/undo/users')
def undo_users(db: Session = Depends(get_session)):
    Seed.undo_users(db)
    return {'message': 'Limpeza dos usuários realizada com sucesso!'}


@router.post('/undo/posts')
def undo_posts(db: Session = Depends(get_session)):
    Seed.undo_posts(db)
    return {'message': 'Limpeza dos posts realizada com sucesso!'}


@router.post('/undo/events')
def undo_events(db: Session = Depends(get_session)):
    Seed.undo_events(db)
    return {'message': 'Limpeza dos eventos realizada com sucesso!'}
