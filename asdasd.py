import os
import sys
import dotenv

from src.auth.ports.context import Users
from src.auth.adapters.orm import ORM, URL

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

dotenv.load_dotenv()
url = URL.create(
    drivername = 'postgresql+asyncpg',
    username = os.getenv('TEST_DATABASE_USERNAME'),
    password = os.getenv('TEST_DATABASE_PASSWORD'),
    host = os.getenv('TEST_DATABASE_HOST'),
    port = os.getenv('TEST_DATABASE_PORT'),
    database = os.getenv('TEST_DATABASE_NAME'))

orm = ORM(url)
users = Users(orm)

async def main():
    async with users:
        await users.accounts.create(username='test', password='test')
        await users.commit()

    async with users:
        account = await users.accounts.read(username='test')
        print(account.username)
        print(account.id)
        await users.accounts.delete(id=account.id)
        await users.commit()


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())