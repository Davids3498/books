import time
import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from src.config import Config
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    url=Config.DB_URL
)


async def init_db():
    retries = 5
    for i in range(retries):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(SQLModel.metadata.create_all)
            print("Database initialized successfully.")
            break  # Exit the loop if successful
        except (asyncpg.exceptions.ConnectionDoesNotExistError, OSError) as e:
            if i < retries - 1:
                print(f"Database connection failed ({e}), retrying in 5 seconds...")
                time.sleep(5)  # Wait before retrying
            else:
                print("Database connection failed. No more retries.")
                raise  # Raise the error if all retries fail


async def get_session() -> AsyncSession:
    Session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with Session() as session:
        yield session