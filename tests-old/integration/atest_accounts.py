import pytest
import socket
from uuid import uuid4
from uuid import UUID

from sqlalchemy import URL
from sqlalchemy import select, insert, update, delete

from src.backend.schemas import ACCOUNT
from src.backend.services import SessionFactory
from src.backend.services import UnitOfWork
from src.users.models import Credentials
from src.users.models import Account

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
    accounts = UnitOfWork(session_factory=SessionFactory(url=url))
    async with accounts:
        try:
            await accounts.create(credentials=Credentials(username='test', password='test'))
            await accounts.commit()
        except LookupError:
            print('Account already in database. Skip')
            pass

    async with accounts:
        try:
            query = select(ACCOUNT).where(ACCOUNT.username == 'test')
            result = await accounts.session.execute(query)
            schema = result.scalars().first()
            assert schema.username == 'test'
        
        finally:
            command = delete(ACCOUNT).where(ACCOUNT.username == 'test')
            await accounts.session.execute(command)
            await accounts.commit()

@pytest.mark.asyncio
async def test_read_account(url : URL):
    accounts = UnitOfWork(session_factory=SessionFactory(url=url))
    identity = uuid4()
    async with accounts:
        command = insert(ACCOUNT).values(id=identity, username='test', password='test')
        await accounts.session.execute(command)
        await accounts.commit()
    
    async with accounts:
        try:
            account = await accounts.read(credentials=Credentials(username='test'))
            assert account.id == identity

        finally:
            command = delete(ACCOUNT).where(ACCOUNT.username == 'test')
            await accounts.session.execute(command)
            await accounts.commit()


@pytest.mark.asyncio
async def test_update_account(url : URL):
    accounts = UnitOfWork(session_factory=SessionFactory(url=url))
    identity = uuid4()

    async with accounts:
        command = insert(ACCOUNT).values(id=identity, username='test', password='test')
        await accounts.session.execute(command)
        await accounts.commit()

    try:
        async with accounts:
            await accounts.update(Account(identity=identity), credentials=Credentials(username='test2'))
            await accounts.commit()

        async with accounts:
            query = select(ACCOUNT).where(ACCOUNT.id==identity)
            result = await accounts.session.execute(query)
            schema = result.scalars().first()
            assert schema.username == 'test2'

    finally:
        async with accounts:
            command = delete(ACCOUNT).where(ACCOUNT.id == identity)
            await accounts.session.execute(command)
            await accounts.commit()


@pytest.mark.asyncio
async def test_delete_account(url : URL):
    accounts = UnitOfWork(session_factory=SessionFactory(url=url))
    identity = uuid4()
    async with accounts:
        command = insert(ACCOUNT).values(id=identity, username='test', password='test')
        await accounts.session.execute(command)
        await accounts.commit()

    async with accounts:
        query = select(ACCOUNT).where(ACCOUNT.username == 'test')
        result = await accounts.session.execute(query)
        schema = result.scalars().first()
        assert schema.username == 'test'

    async with accounts:
        await accounts.delete(account=Account(identity=identity))
        await accounts.commit()

    async with accounts:
        query = select(ACCOUNT).where(ACCOUNT.username == 'test')
        result = await accounts.session.execute(query)
        schema = result.scalars().first()
        assert schema is None