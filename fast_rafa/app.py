from fastapi import FastAPI

from fast_rafa.routes.category import router as category_router
from fast_rafa.routes.favorite import router as favorite_router
from fast_rafa.routes.organization import router as organization_router
from fast_rafa.routes.post import router as post_router
from fast_rafa.routes.user import router as user_router

app = FastAPI(
    title='fast_rafa',
    version='0.1.0',
    description='API para o projeto fast_rafa',
)

app.version = '1'

app.include_router(
     organization_router,
     prefix='/api/v' + app.version + '/organizations',
     tags=['Organizations']
 )


app.include_router(user_router,
                   prefix='/api/v' + app.version + '/users',
                   tags=['Users'])


app.include_router(
    category_router,
    prefix='/api/v' + app.version + '/categories',
    tags=['Categories']
)

app.include_router(post_router,
                   prefix='/api/v' + app.version + '/posts',
                   tags=['Posts'])

app.include_router(
    favorite_router,
    prefix='/api/v' + app.version + '/favorites',
    tags=['Favorites']
)
