from typing import AsyncIterator

import httpx
import pytest
import pytest_asyncio
from fastapi import FastAPI

from src.auth.services import JWTAuth

@pytest_asyncio.fixture()
async def client() -> AsyncIterator[httpx.AsyncClient]:
    api = FastAPI()
    jwt_auth = JWTAuth(prefix='/auth', settings=None)
    api.include_router(jwt_auth.router)
    async with httpx.AsyncClient(app=api, base_url='http://testserver') as client:
        yield client

@pytest.mark.asyncio
async def test_register(client : httpx.AsyncClient) -> None:
    form_data = {'username': 'test', 'password': 'test'}
    response = await client.post('/auth/register', data=form_data)
    assert response.status_code == 200