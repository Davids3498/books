from fastapi import FastAPI, Query
from api.endpoints.Book import book_router
from contextlib import asynccontextmanager
from db.database import init_db
version = 'V1'


@asynccontextmanager
async def life_span(app: FastAPI):
    print("running...")
    await init_db()
    yield 
    print("stopped...")

    
app = FastAPI(version=version, lifespan=life_span)

app.include_router(book_router, prefix=f'/api/{version}/books')
