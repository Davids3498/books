from fastapi import APIRouter, Depends

from src.api.dependencies.dependency import get_current_user
from src.db.database import get_session
from src.db.models.User import User
from src.models.Review import ReviewCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.services.ReviewService import ReviewService
review_router = APIRouter(tags=["Reviews"])

review_service = ReviewService()


@review_router.post("/book/{book_uid}")
async def add_review_to_book(book_uid: str,  review_data: ReviewCreateModel, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    new_review = await review_service.add_new_review(user.email, book_uid, review_data, session)
    return new_review


@review_router.get("/")
async def get_all_user_reviews(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    new_review = await review_service.add_new_review(user.uid, session)
    return new_review
