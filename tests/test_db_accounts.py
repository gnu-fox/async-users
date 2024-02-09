import pytest
import socket
import warnings

from uuid import uuid4
from uuid import UUID

from sqlalchemy import URL
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.backend.schemas import Account
from src.backend.gateway import Accounts
from src.backend.services import SessionFactory
from src.backend.services import UnitOfWork

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
async def test_accounts(url : URL):
    engine = create_async_engine(url, future=True)
    session_factory = async_sessionmaker(engine, class_=AsyncSession)
    session = session_factory()
    accounts = Accounts(session)

    await session.begin()
    try:
        account_id = await accounts.create(username='test', password='test')
        assert isinstance(account_id, UUID)
        await session.commit()
    except:
        warnings.warn('test_accounts: failed to create account')
        await session.rollback()


    account_id = await accounts.read(username='test')
    assert isinstance(account_id, UUID)

    await accounts.update(account_id, username='test2')
    await session.commit()

    account_id = await accounts.read(username='test2')
    assert isinstance(account_id, UUID)

    await accounts.delete(account_id)
    await session.commit()

    await session.close()
    await engine.dispose()

@pytest.mark.asyncio
async def test_unit_of_work(url : URL):
    session_factory = SessionFactory(url)

    try:
        async with UnitOfWork(session_factory) as uow:
            account_id = await uow.accounts.create(username='test', password='test')
            assert isinstance(account_id, UUID)

        async with UnitOfWork(session_factory) as uow:
            account_id = await uow.accounts.read(username='test')
            assert isinstance(account_id, UUID)

        async with UnitOfWork(session_factory) as uow:
            await uow.accounts.update(account_id, username='test2')
            account_id = await uow.accounts.read(username='test2')
            assert isinstance(account_id, UUID)

        async with UnitOfWork(session_factory) as uow:
            await uow.accounts.delete(account_id)

    except:
        engine = create_async_engine(url, future=True)
        session_factory = async_sessionmaker(engine, class_=AsyncSession)
        session = session_factory()
        async with session.begin():
            statement = delete(Account).where(Account.username == 'test')
            await session.execute(statement)
        await session.close()
        await engine.dispose()