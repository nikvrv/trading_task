from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import settings
from sqlalchemy.ext.asyncio import AsyncEngine
from src.db.models import Base

# DATABASE_URL = settings.database_url
# DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"
DATABASE_URL = "sqlite+aiosqlite:///../test.db"

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)



async def get_db():
    async with SessionLocal() as session:
        """
        For routes with DI
        """
        yield session


async def get_db_session() -> AsyncSession:
    """
    For events
    :return:
    """
    async_session = SessionLocal()
    return async_session



async def create_tables(db_engine: AsyncEngine):
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

