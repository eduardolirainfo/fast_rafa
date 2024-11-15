from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from fast_rafa.database import get_session
from fast_rafa.models import User
from fast_rafa.security import get_current_user
from fast_rafa.utils import (
    accepted_file,
    generate_unique_file,
    hash_password,
    save_file_locally,
    verify_password,
)

auth_routes = APIRouter()


@auth_routes.get('/')
async def authenticate(current_user: User = Depends(get_current_user)):
    if current_user:
        return {'id': current_user.id, 'email': current_user.email}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized'
    )


@auth_routes.post('/images')
async def image_validation(image: UploadFile = File(...)):
    if not accepted_file(image.filename):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='File type not permitted',
        )

    image.filename = generate_unique_file(image.filename)
    upload = save_file_locally(image)
    if 'url' not in upload:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Upload failed'
        )

    return {'imageUrl': upload['url']}


@auth_routes.post('/signup')
async def sign_up(
    email: str, password: str, db: Session = Depends(get_session)
):
    hashed_password = hash_password(password)
    user = User(email=email, password=hashed_password)
    db.add(user)
    db.commit()
    return {'id': user.id, 'email': user.email}


@auth_routes.post('/login')
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session),
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials',
        )
    return {'access_token': 'token_example', 'token_type': 'bearer'}


@auth_routes.get('/logout')
async def logout():
    response = JSONResponse(content={'message': 'The user has logged out.'})
    response.delete_cookie('access_token')
    return response


@auth_routes.get('/unauthorized')
async def unauthorized():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized'
    )
