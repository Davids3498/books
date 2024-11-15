from typing import List, Optional
import uuid
from datetime import date, datetime
import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Field, SQLModel, Column, Relationship


class Book(SQLModel, table=True):
    __tablename__ = "books"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False,
                         primary_key=True, default=uuid.uuid4)
    )
    title: str
    author: str
    publisher: str
    published_date: date
    user_uid: Optional[uuid.UUID] = Field(
        default=None, foreign_key="users.uid")
    page_count: int
    language: str
    created_at: datetime = Field(sa_column=Column(
        pg.TIMESTAMP, default=datetime.now))
    update_at: datetime = Field(sa_column=Column(
        pg.TIMESTAMP, default=datetime.now))

    user: Optional["User"] = Relationship(back_populates="books")
    reviews: Optional[List["Review"]] = Relationship(back_populates="book", sa_relationship_kwargs={'lazy': 'selectin'})

    def __repr__(self):
        return f"<Book {self.title}>"
