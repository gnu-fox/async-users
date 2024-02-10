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
    uow = UnitOfWork(session_factory=SessionFactory(url=url))
    async with uow:
        try:
            await uow.create(credentials=Credentials(username='test', password='test'))
            await uow.commit()
        except LookupError:
            print('Account already in database. Skip')
            pass

    async with uow:
        try:
            query = select(ACCOUNT).where(ACCOUNT.username == 'test')
            result = await uow.session.execute(query)
            schema = result.scalars().first()
            assert schema.username == 'test'
        
        finally:
            command = delete(ACCOUNT).where(ACCOUNT.username == 'test')
            await uow.session.execute(command)
            await uow.commit()

@pytest.mark.asyncio
async def test_read_account(url : URL):
    uow = UnitOfWork(session_factory=SessionFactory(url=url))
    identity = uuid4()
    async with uow:
        command = insert(ACCOUNT).values(id=identity, username='test', password='test')
        await uow.session.execute(command)
        await uow.commit()
    
    async with uow:
        try:
            account = await uow.read(credentials=Credentials(username='test'))
            assert account.id == identity

        finally:
            command = delete(ACCOUNT).where(ACCOUNT.username == 'test')
            await uow.session.execute(command)
            await uow.commit()


@pytest.mark.asyncio
async def test_update_account(url : URL):
    uow = UnitOfWork(session_factory=SessionFactory(url=url))
    identity = uuid4()

    async with uow:
        command = insert(ACCOUNT).values(id=identity, username='test', password='test')
        await uow.session.execute(command)
        await uow.commit()

    try:
        async with uow:
            await uow.update(Account(identity=identity), credentials=Credentials(username='test2'))
            await uow.commit()

        async with uow:
            query = select(ACCOUNT).where(ACCOUNT.id==identity)
            result = await uow.session.execute(query)
            schema = result.scalars().first()
            assert schema.username == 'test2'

    finally:
        async with uow:
            command = delete(ACCOUNT).where(ACCOUNT.id == identity)
            await uow.session.execute(command)
            await uow.commit()


@pytest.mark.asyncio
async def test_delete_account(url : URL):
    uow = UnitOfWork(session_factory=SessionFactory(url=url))
    identity = uuid4()
    async with uow:
        command = insert(ACCOUNT).values(id=identity, username='test', password='test')
        await uow.session.execute(command)
        await uow.commit()

    async with uow:
        query = select(ACCOUNT).where(ACCOUNT.username == 'test')
        result = await uow.session.execute(query)
        schema = result.scalars().first()
        assert schema.username == 'test'

    async with uow:
        await uow.delete(account=Account(identity=identity))
        await uow.commit()

    async with uow:
        query = select(ACCOUNT).where(ACCOUNT.username == 'test')
        result = await uow.session.execute(query)
        schema = result.scalars().first()
        assert schema is None