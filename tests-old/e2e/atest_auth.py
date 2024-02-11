import pytest
import socket
from uuid import uuid4
from uuid import UUID
from typing import AsyncIterator

import httpx
import pytest
import pytest_asyncio
from sqlalchemy import URL
from sqlalchemy import select, insert, update, delete
from fastapi import FastAPI

from src.settings import Settings
from src.auth.router import Auth
from src.backend.schemas import ACCOUNT
from src.backend.services import SessionFactory
from src.backend.services import UnitOfWork
from src.users.models import Credentials, SecretStr
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

@pytest.fixture
def anyio_backend() -> str:
    return 'asyncio'

@pytest_asyncio.fixture()
async def client(url : URL) -> AsyncIterator[httpx.AsyncClient]:
    api = FastAPI()
    auth = Auth(prefix='/auth', settings = Settings(database_url=url))
    auth.mount(api)

    async with httpx.AsyncClient(app=api, base_url='http://testserver') as client:
        yield client

@pytest.mark.asyncio
async def test_login(client : httpx.AsyncClient, url : URL) -> None:
    uow = UnitOfWork(session_factory=SessionFactory(url=url))
    async with uow:
        try:
            account = await uow.accounts.create(credentials = Credentials(username='test', password=SecretStr('test')))
            await uow.commit()

            form_data = {'username': 'test', 'password': 'test'}
            response = await client.post('/auth/login', data=form_data)
            assert response.status_code == 200

        finally:
            await uow.accounts.delete(account)


@pytest.mark.asyncio
async def test_register(client : httpx.AsyncClient, url : URL) -> None:
    uow = UnitOfWork(session_factory=SessionFactory(url=url))
    async with uow:
        try:
            form_data = {'username' : 'test', 'password' : 'test'}
            response = await client.post('/auth/register', data=form_data)
            assert response.status_code == 200

            account = await uow.accounts.read(credentials = Credentials(username='test', password=SecretStr('test')))
            assert account
        finally:
            await uow.accounts.delete(account)