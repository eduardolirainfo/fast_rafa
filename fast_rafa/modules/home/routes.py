import pytz
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from fast_rafa.core.security import get_current_user
from fast_rafa.modules.users.models import (
    User,
)

timezone = pytz.timezone('America/Sao_Paulo')

router = APIRouter()

templates = Jinja2Templates(directory='fast_rafa/templates')


@router.get('/', response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})
