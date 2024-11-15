from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from src.db.database import get_session
from src.models.Book import Book, BookCreateModel, BookDetailModel, BookUpdateModel
from src.services.BookService import BookService
from src.api.dependencies.dependency import AccessTokenBearer, RoleChecker

role_checker = Depends(RoleChecker(["admin", "user"]))
# book_router = APIRouter(tags=["Books"], dependencies=[role_checker])
book_router = APIRouter(tags=["Books"])
book_service = BookService()
access_token_bearer = AccessTokenBearer()


@book_router.get("/", response_model=List[Book])
async def get_all_books(session: AsyncSession = Depends(get_session)):
    books = await book_service.get_all_books(session)
    return books


@book_router.get("/user/{user_uid}", response_model=List[Book])
async def get_user_books_submissions(user_uid: str, session: AsyncSession = Depends(get_session)):
    books = await book_service.get_user_books(user_uid, session)
    return books


@book_router.get("/{book_uid}", response_model=BookDetailModel)
async def get_book(book_uid: str, session: AsyncSession = Depends(get_session)) -> dict:
    book = await book_service.get_book(book_uid, session)

    if book:
        return book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="book ont found")


# async def create_book(book_data: BookCreateModel, session: AsyncSession = Depends(get_session), token_details: dict = Depends(access_token_bearer)) -> dict:
@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_book(book_data: BookCreateModel, session: AsyncSession = Depends(get_session), token_details: dict = Depends(access_token_bearer)) -> dict:
    user_uid = token_details.get("user")["user_uid"]
    user_uid = 3
    new_book = await book_service.create_book(book_data, user_uid, session)
    return new_book


@book_router.patch("/{book_uid}", response_model=Book)
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
