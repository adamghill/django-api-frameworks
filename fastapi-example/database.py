from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db:5432/django-api-frameworks"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_size=5,
    max_overflow=3,
    pool_timeout=30,
    pool_recycle=1800,
)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # async with engine.begin() as conn:  # startup, create tables
    #     await conn.run_sync(Base.metadata.create_all)

    yield  # server is running and handling requests

    await engine.dispose()  # server shut down


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
