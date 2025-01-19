from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from fast_rafa.modules.auth.routes import router as token_router
from fast_rafa.modules.calendars.routes import router as calendar_router
from fast_rafa.modules.categories.routes import router as category_router
from fast_rafa.modules.categories_main.routes import (
    router as category_main_router,
)
from fast_rafa.modules.deliveries.routes import router as delivery_router
from fast_rafa.modules.events.routes import router as event_router
from fast_rafa.modules.favorites.routes import router as favorite_router
from fast_rafa.modules.main.routes import router as main_router
from fast_rafa.modules.messages.routes import router as message_router
from fast_rafa.modules.organizations.routes import (
    router as organization_router,
)
from fast_rafa.modules.posts.routes import router as post_router
from fast_rafa.modules.seeds.routes import router as seed_router
from fast_rafa.modules.uploads.routes import router as upload_router
from fast_rafa.modules.users.routes import router as user_router
from fast_rafa.modules.watchlists.routes import router as watchlist_router
 

app = FastAPI(
    title='fast_rafa',
    version='0.1.0',
    description='API para o projeto fast_rafa',
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # Ou seu domínio específico
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


app.version = '1'


app.mount(
    '/static',
    StaticFiles(directory='fast_rafa/static'),
    name='static',
)
app.mount(
    '/uploads',
    StaticFiles(directory='fast_rafa/static/img/uploads'),
    name='uploads',
)


app.include_router(
    organization_router,
    prefix='/api/v' + app.version + '/organizations',
    tags=['Organizations'],
)


app.include_router(
    user_router, prefix='/api/v' + app.version + '/users', tags=['Users']
)


app.include_router(
    category_router,
    prefix='/api/v' + app.version + '/categories',
    tags=['Categories'],
)

app.include_router(
    post_router, prefix='/api/v' + app.version + '/posts', tags=['Posts']
)

app.include_router(
    favorite_router,
    prefix='/api/v' + app.version + '/favorites',
    tags=['Favorites'],
)


app.include_router(
    calendar_router,
    prefix='/api/v' + app.version + '/calendars',
    tags=['Calendars'],
)

app.include_router(
    delivery_router,
    prefix='/api/v' + app.version + '/deliveries',
    tags=['Deliveries'],
)

app.include_router(
    watchlist_router,
    prefix='/api/v' + app.version + '/watchlist',
    tags=['Watchlist'],
)

app.include_router(
    event_router, prefix='/api/v' + app.version + '/events', tags=['Events']
)


app.include_router(
    message_router,
    prefix='/api/v' + app.version + '/messages',
    tags=['Messages'],
)


app.include_router(token_router, tags=['auth'])

app.include_router(
    seed_router, prefix='/api/v' + app.version + '/seeds', tags=['Seed']
)

app.include_router(
    category_main_router,
    prefix='/api/v' + app.version + '/categories_main',
    tags=['Categories Main'],
)


app.include_router(
    upload_router, prefix='/api/v' + app.version + '/uploads', tags=['Uploads']
)

app.include_router(main_router, tags=['Main'])
