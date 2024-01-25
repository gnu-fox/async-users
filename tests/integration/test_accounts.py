import os
import dotenv
import pytest

from src.auth.domain.models import SecretStr
from src.auth.adapters.async_sqlalchemy.crud import ORM, Accounts, URL

dotenv.load_dotenv()

@pytest.fixture(scope='class')
def database_url() -> URL:
    url = URL.create(
        drivername = 'postgresql+psycopg2',
        username = os.getenv('TEST_DATABASE_USERNAME'),
        password = os.getenv('TEST_DATABASE_PASSWORD'),
        host = os.getenv('TEST_DATABASE_HOST'),
        port = os.getenv('TEST_DATABASE_PORT'),
        database = os.getenv('TEST_DATABASE_NAME'))
    return url

@pytest.fixture(scope='class')
async def orm(database_url : URL) -> ORM:
    async with ORM(database_url) as orm:
        yield orm

async def test_accounts(orm : ORM):
    async with orm as session:
        accounts = Accounts(session)
        await accounts.create(username='test', password=SecretStr('test'))
        account = await accounts.read(username='test')
        assert account.username == 'test'
        await accounts.delete(id=account.id)
        account = await accounts.read(username='test')
        assert account is None

    