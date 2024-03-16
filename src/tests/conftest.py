import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from core.db.model import Base


@pytest.fixture(scope='module')
async def engine():
    engine = create_async_engine('sqlite+aiosqlite:///:memory:', echo=True)
    yield engine
    await engine.dispose()

@pytest.fixture(scope='module')
async def session(engine):
    async_session = async_sessionmaker(bind=engine, class_=AsyncSession)
    
    # Create tables in the database
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield async_session
    
    # Rollback any uncommitted changes and close the session
    async with async_session() as session:
        await session.rollback()
        await session.close()
