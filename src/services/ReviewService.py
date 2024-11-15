from fastapi import HTTPException
from fastapi import status
from sqlmodel import desc, select
from src.db.models.Review import Review
from src.models.Review import ReviewCreateModel
from src.services.UserService import UserService
from src.services.BookService import BookService
from sqlmodel.ext.asyncio.session import AsyncSession

book_service = BookService()
user_service = UserService()


class ReviewService:
    async def add_new_review(self, user_email: str, book_uid: str, review_data: ReviewCreateModel, session: AsyncSession):
        try:
            book = await book_service.get_book(book_uid, session)
            if not book:
                raise HTTPException(status.HTTP_404_NOT_FOUND,
                                    detail="Book does not exists.")

            user = await user_service.get_user_by_email(user_email, session)
            if not user:
                raise HTTPException(status.HTTP_404_NOT_FOUND,
                                    detail="User does not exists.")

            review_data_dict = review_data.model_dump()
            new_review = Review(**review_data_dict)
            new_review.user = user

            new_review.book = book

            session.add(new_review)

            await session.commit()

            return new_review

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Oops...")

    async def get_all_user_reviews(self, user_uid: str, session: AsyncSession):
        try:
            statement = select(Review).where(Review.user_uid == user_uid).order_by(desc(Review.created_at))

            result = await session.exec(statement)

            return result.all()

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Oops...")
