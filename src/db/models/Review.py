from typing import Optional
import uuid
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Field, SQLModel, Column, Relationship


class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False,
                         primary_key=True, default=uuid.uuid4)
    )
    rating: int = Field(lt=5)
    review_text: str
    user_uid: Optional[uuid.UUID] = Field(
        default=None, foreign_key="users.uid")
    book_uid: Optional[uuid.UUID] = Field(
        default=None, foreign_key="books.uid")
    created_at: datetime = Field(sa_column=Column(
        pg.TIMESTAMP, default=datetime.now))
    update_at: datetime = Field(sa_column=Column(
        pg.TIMESTAMP, default=datetime.now))
    user: Optional["User"] = Relationship(back_populates="reviews")
    book: Optional["Book"] = Relationship(back_populates="reviews")

    def __repr__(self):
        return f"<Review {self.rating}>"
