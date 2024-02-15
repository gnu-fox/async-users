from uuid import uuid4
import pytest
import socket
from typing import AsyncIterator

import httpx
import pytest
import pytest_asyncio
from fastapi import FastAPI

from src.auth.models import Credentials, Account, SecretStr
from src.auth.services import URL, Users, Settings, Auth

@pytest.fixture
def url() -> URL:
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
    uow = Users(settings = Settings(database_url=url))
    account = Account(id=uuid4())
    async with uow:
        existent = await uow.accounts.read(credentials = Credentials(username='test'))
        if existent:
            await uow.accounts.delete(existent)
            
        await uow.accounts.create(account = account, credentials = Credentials(username='test', password=SecretStr('test')))
        await uow.commit()

        form_data = {'username': 'test', 'password': 'test'}
        response = await client.post('/auth/login', data=form_data)
        
        assert response.status_code == 200
        await uow.accounts.delete(account)
        


@pytest.mark.asyncio
async def test_register(client : httpx.AsyncClient, url : URL) -> None:
    uow = Users(settings = Settings(database_url=url))
    async with uow:

        existent = await uow.accounts.read(credentials = Credentials(username='test'))
        if existent:
            await uow.accounts.delete(existent)

        form_data = {'username' : 'test', 'password' : 'test'}
        response = await client.post('/auth/register', data=form_data)
        assert response.status_code == 200

        account = await uow.accounts.read(credentials = Credentials(username='test', password=SecretStr('test')))
        assert account
        await uow.accounts.delete(account)