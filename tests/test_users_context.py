import os
import dotenv
import pytest

pytest_plugins = ('pytest_asyncio',)

from src.users.adapters.orm import URL, ORM
from src.users.services.users import Users

@pytest.fixture
def url()->URL:
    dotenv.load_dotenv()

    return URL.create(
        drivername='postgresql+asyncpg',
        username=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASSWORD'),
        host=os.getenv('DATABASE_HOST'),
        port=os.getenv('DATABASE_PORT'), 
        database=os.getenv('DATABASE_NAME')
    )

@pytest.mark.asyncio
async def test_users_context(url : URL):

    orm = ORM(url=url)
    users = Users(orm=orm)

    async with users:
        user = await users.create(username='test', password='test')
        await users.commit()
        
    async with users:
        user = await users.read(username='test')
        assert user.username == 'test'

    async with users:
        await users.delete(username='test')
        await users.commit()