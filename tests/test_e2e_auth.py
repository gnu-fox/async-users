from typing import AsyncIterator

import httpx
import pytest, pytest_asyncio

from fastapi import FastAPI

from src.auth.router import Auth

@pytest.fixture
def anyio_backend() -> str:
    return 'asyncio'

@pytest_asyncio.fixture()
async def client() -> AsyncIterator[httpx.AsyncClient]:
    api = FastAPI()
    auth = Auth(prefix='/auth')
    auth.mount(api)

    async with httpx.AsyncClient(app=api, base_url='http://testserver') as client:
        yield client

@pytest.mark.asyncio
async def test_login(client : httpx.AsyncClient) -> None:
    form_data = {'username': 'test', 'password': 'test'}
    response = await client.post('/auth/login', data=form_data)
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_register(client : httpx.AsyncClient) -> None:
    form_data = {'username' : 'patroclio', 'password' : 'patroclio_capo_total'}
    response = await client.post('/auth/register', data=form_data)
    assert response.status_code == 200