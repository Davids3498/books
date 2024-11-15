from fastapi import FastAPI, Query
from src.api.endpoints.Book import book_router
from src.api.endpoints.Auth import auth_router
from src.api.endpoints.GoogleAuth import google_auth_router
from src.api.endpoints.Review import review_router
from contextlib import asynccontextmanager
from src.db.database import init_db
from src.middleware import register_middleware
from starlette.middleware.sessions import SessionMiddleware
version = 'V1'
from src.config import Config


@asynccontextmanager
async def life_span(app: FastAPI):
    print("running...")
    await init_db()
    yield
    print("stopped...")


app = FastAPI(version=version, lifespan=life_span)
app.add_middleware(SessionMiddleware, secret_key=Config.SECRET_KEY)

register_middleware(app)

app.include_router(book_router, prefix=f'/api/{version}/books')
app.include_router(auth_router, prefix=f'/api/{version}/auth')
app.include_router(review_router, prefix=f'/api/{version}/reviews')
app.include_router(google_auth_router)
