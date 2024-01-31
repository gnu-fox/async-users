import os
import dotenv
import pytest

from src.users.adapters.db_provider import URL, ORM, Provider
from src.users.ports.utils import Repository

dotenv.load_dotenv()
url = URL.create(
        drivername='postgresql+asyncpg',
        username=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASSWORD'),
        host=os.getenv('DATABASE_HOST'),
        port=os.getenv('DATABASE_PORT'), 
        database=os.getenv('DATABASE_NAME')
    )

class Users(Repository):
    def __init__(self, provider : Provider):
        super().__init__(provider.session_factory)
        self.accounts = provider.accounts
        self.credentials = provider.credentials


async def main():
    orm = ORM(url=url)
    users = Users(provider=Provider(orm=orm))

    async with users:
        print()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())


