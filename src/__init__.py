from fastapi import FastAPI, Query
from .Books.routes import book_router

version = 'V1'

app = FastAPI(version=version)

app.include_router(book_router, prefix=f'/api/{version}/books')
