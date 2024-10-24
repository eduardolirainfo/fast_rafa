from http import HTTPStatus

from fastapi import APIRouter

from fast_rafa.models import Message

router = APIRouter()  # Use APIRouter aqui


@router.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olar mundo!'}
