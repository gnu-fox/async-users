import pytest
import socket
from uuid import uuid4
from uuid import UUID

from sqlalchemy import URL
from sqlalchemy import select, insert, update, delete

from src.adapters.data_schemas import ACCOUNT
from src.adapters.unit_of_work import SessionFactory, UnitOfWork
from src.domain.models import Credentials
from src.domain.models import Account

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
async def test_create_account(url : URL):
    uow = UnitOfWork(session_factory=SessionFactory(url=url))
    async with uow:
        try:
            await uow.accounts.create(credentials=Credentials(username='test', password='test'))
            await uow.commit()
        except Exception:
            print('Account already in database. Skip')
            pass

    async with uow:
        try:
            query = select(ACCOUNT).where(ACCOUNT.username == 'test')
            result = await uow.accounts.session.execute(query)
            schema = result.scalars().first()
            assert schema.username == 'test'
        
        finally:
            command = delete(ACCOUNT).where(ACCOUNT.username == 'test')
            await uow.accounts.session.execute(command)
            await uow.commit()


@pytest.mark.asyncio
async def test_read_account(url : URL):
    uow = UnitOfWork(session_factory=SessionFactory(url=url))
    identity = uuid4()
    async with uow:
        try:
            command = insert(ACCOUNT).values(id=identity, username='test', password='test')
            await uow.accounts.session.execute(command)
            await uow.commit()        
        except Exception:
            print('Account already in database. Skip')
            pass
    
    async with uow:
        try:
            account = await uow.accounts.read(credentials=Credentials(username='test'))
            assert account.id == identity

        finally:
            command = delete(ACCOUNT).where(ACCOUNT.username == 'test')
            await uow.accounts.session.execute(command)
            await uow.commit()


@pytest.mark.asyncio
async def test_update_account(url : URL):
    uow = UnitOfWork(session_factory=SessionFactory(url=url))
    identity = uuid4()

    async with uow:
        try:
            command = insert(ACCOUNT).values(id=identity, username='test', password='test')
            await uow.accounts.session.execute(command)
            await uow.commit()        
        except Exception:
            print('Account already in database. Skip')
            pass
    
    try:
        async with uow:
            await uow.accounts.update(Account(id=identity), credentials=Credentials(username='test2'))
            await uow.commit()

        async with uow:
            query = select(ACCOUNT).where(ACCOUNT.id==identity)
            result = await uow.accounts.session.execute(query)
            schema = result.scalars().first()
            assert schema.username == 'test2'

    finally:
        async with uow:
            command = delete(ACCOUNT).where(ACCOUNT.id == identity)
            await uow.accounts.session.execute(command)
            await uow.commit()


@pytest.mark.asyncio
async def test_delete_account(url : URL):
    uow = UnitOfWork(session_factory=SessionFactory(url=url))
    identity = uuid4()
    async with uow:
        try:
            command = insert(ACCOUNT).values(id=identity, username='test', password='test')
            await uow.accounts.session.execute(command)
            await uow.commit()        
        except Exception:
            print('Account already in database. Skip')
            pass
    

    async with uow:
        query = select(ACCOUNT).where(ACCOUNT.username == 'test')
        result = await uow.accounts.session.execute(query)
        schema = result.scalars().first()
        assert schema.username == 'test'

    async with uow:
        await uow.accounts.delete(account=Account(id=identity))
        await uow.commit()

    async with uow:
        query = select(ACCOUNT).where(ACCOUNT.username == 'test')
        result = await uow.accounts.session.execute(query)
        schema = result.scalars().first()
        assert schema is None