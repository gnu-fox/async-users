import os
import dotenv
import pytest

from src.auth.domain.models import SecretStr
from src.auth.ports.context import Users
from src.auth.adapters.sqlalchemy.orm import ORM as SqlAlchemyORM, URL

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
def users(database_url : URL) -> Users:
    yield Users(orm=SqlAlchemyORM(url=database_url))


def test_accounts_crud(users : Users):
    with users:
        users.accounts.crud.create(username='test', password=SecretStr('test'))
        users.commit()
    
    with users:
        account = users.accounts.crud.read(username='test')
        assert account.username == 'test'
        assert account.verify(SecretStr('test')) == True
        assert account.verify(SecretStr('test2')) == False
    
    with users:
        users.accounts.crud.delete(id=account.id)
        users.commit()

    with users:
        assert users.accounts.crud.read(username='test') == None
        users.rollback()
