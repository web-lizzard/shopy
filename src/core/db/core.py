from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from core.configuration import configuration

DATABASE_ENGINE = create_async_engine(str(configuration.database.url))
DEFAULT_SESSION_MAKER = async_sessionmaker(
    bind=DATABASE_ENGINE, expire_on_commit=True, class_=AsyncSession
)
