import pytest
import socket

from sqlalchemy import URL
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

@pytest.fixture
def url():
    return URL.create(
        drivername = 'postgresql+asyncpg',
        username = 'postgres',
        password = 'postgres',
        host = socket.gethostbyname('postgres'),
        port = 5432,
        database = 'postgres'
    )

@pytest.mark.asyncio
async def test_database_connection(url : URL):
    engine = create_async_engine(url)
    session_factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with session_factory() as session:
        async with session.begin():
            result = await session.execute(select(1))