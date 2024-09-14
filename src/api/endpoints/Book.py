from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from db.database import get_session
from models.Book import BookModel, BookCreateModel, BookUpdateModel
from services.BookService import BookService
book_router = APIRouter()

book_service = BookService()


@book_router.get("/", response_model=List[BookModel])
async def get_all_books(session: AsyncSession = Depends(get_session)):
    books = await book_service.get_all_books(session)
    return books


@book_router.get("/{book_uid}",response_model=BookModel)
async def get_book(book_uid: str, session: AsyncSession = Depends(get_session)) -> dict:
    book = await book_service.get_book(book_uid, session)

    if book:
        return book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="book ont found")


@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=BookModel)
async def create_book(book_data: BookCreateModel, session: AsyncSession = Depends(get_session)) -> dict:
    new_book = await book_service.create_book(book_data, session)
    return new_book


@book_router.patch("/{book_uid}", response_model=BookModel)
async def update_book(book_uid: str, book_update_data: BookUpdateModel, session: AsyncSession = Depends(get_session)) -> dict:
    updated_book = await book_service.update_book(book_uid, book_update_data, session)

    if updated_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="book ont found")
    else:
        return updated_book


@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session)):
    book_to_delete = await book_service.delete_book(book_uid, session)

    if book_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="book ont found")
    else:
        return {}
