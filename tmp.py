import os
import sys
import dotenv

dotenv.load_dotenv()

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.users.adapters.orm import URL, ORM
from src.users.services.users import Users

url = URL.create(
    drivername='postgresql+asyncpg',
    username=os.getenv('DATABASE_USER'),
    password=os.getenv('DATABASE_PASSWORD'),
    host=os.getenv('DATABASE_HOST'),
    port=os.getenv('DATABASE_PORT'), 
    database=os.getenv('DATABASE_NAME')
)

orm = ORM(url=url)

users = Users(orm=orm)

async def main():
    async with users:
        user = await users.create(username='test', password='test')
        users.commit()
        
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())