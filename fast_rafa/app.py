from fastapi import FastAPI

from fast_rafa.routes.auth import router as token_router
from fast_rafa.routes.calendar import router as calendar_router
from fast_rafa.routes.category import router as category_router
from fast_rafa.routes.delivery import router as delivery_router
from fast_rafa.routes.event import router as event_router
from fast_rafa.routes.favorite import router as favorite_router
from fast_rafa.routes.message import router as message_router
from fast_rafa.routes.organization import router as organization_router
from fast_rafa.routes.post import router as post_router
from fast_rafa.routes.seed import router as seed_router
from fast_rafa.routes.user import router as user_router
from fast_rafa.routes.watchlist import router as watchlist_router

app = FastAPI(
    title='fast_rafa',
    version='0.1.0',
    description='API para o projeto fast_rafa',
)

app.version = '1'

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

app.include_router(seed_router, prefix='/api/v' + app.version, tags=['Seed'])
