import os
import dotenv
import pytest

from src.users.adapters.db_provider import URL, ORM
from src.users.adapters.db_provider import Accounts, Credentials
from src.users.ports.utils import Repository
 
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

class Users(Repository):
    def __init__(self):
        super().__init__()
        self.accounts = Accounts()
        self.credentials = Credentials()

@pytest.mark.asyncio
async def test_accounts(url : URL):
    print(url)

    orm=ORM(url=url)
    Users.session_factory = orm.session_factory
    users = Users()
    
    async with users:
        await users.accounts.create(username='test', password='test')
        await users.commit()
        
    async with users:
        account = await users.accounts.read(username='test')
        assert await users.credentials.verify(account.id, 'test')
        assert account.username == 'test'
    
    async with users:
        await users.accounts.delete(id=account.id)
        await users.commit()

        account = await users.accounts.read(username='test')
        assert account is None

    await users.close()
        




    

