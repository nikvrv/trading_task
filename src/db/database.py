from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import get_settings
from sqlalchemy.ext.asyncio import AsyncEngine
from src.db.models import Base

settings = get_settings()

engine = create_async_engine(settings.database_url, echo=True)
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

