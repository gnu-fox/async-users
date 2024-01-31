import os
import dotenv
import pytest

pytest_plugins = ('pytest_asyncio',)

from src.users.adapters.db_provider import URL, ORM
from src.users.adapters.accounts import Accounts

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
async def test_accounts(url : URL):

    orm = ORM(url=url)
    session_factory = orm.session_factory
    session = session_factory()

    async with session:
        accounts = Accounts(session=session)
        try:
            await accounts.create(username='test', password='test')
            await session.commit()
        except Exception as e:
            await session.rollback()
        
    async with session:
        account = await accounts.read(username='test')
        assert account.username == 'test'

    
    async with session:
        await accounts.delete(id=account.id)
        await session.commit()

        account = await accounts.read(username='test')
        assert account is None

    await session.close()
    await orm.dispose()



