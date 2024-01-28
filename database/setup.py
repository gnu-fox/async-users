import os
import socket

import asyncio
import asyncpg
from asyncpg import Pool

def uri(user: str, password: str, host: str, database: str, port: str = '5432') -> str:
    return f'postgresql://{user}:{password}@{host}:{port}/{database}'

async def database_connect(dns):
    await asyncio.sleep(10)
    while True:
        try:
            connection = await asyncpg.connect(dsn=dns)
            print("Database connection established.")
            return connection
        except asyncpg.exceptions.CannotConnectNowError as e:
            print(f"Failed to connect to the database. Retrying... Error: {e}")
            await asyncio.sleep(5)  # Wait for 5 seconds before retrying

async def migrate(sql_script : str, connection_pool : Pool) :
    async with connection_pool.acquire() as connection:
        await connection.execute(sql_script)
    
async def setup_database(dns : str):
    await database_connect(dns)
    pool = await asyncpg.create_pool(dsn=DNS)
    migrations = os.listdir(MIGRATIONS_PATH)
    for migration in sorted(migrations):
        print(f'Running migration: {migration}')
        with open(f'{MIGRATIONS_PATH}/{migration}', 'r') as file:
            script = file.read()
            await migrate(script, pool)
        print(f'Finished migration: {migration}')

if __name__ == '__main__':
    MIGRATIONS_PATH = 'database/migrations'

    DATABASE_USER = os.environ.get('DATABASE_USER')
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
    DATABASE_HOST = socket.gethostbyname('postgres')
    DATABASE_NAME = os.environ.get('DATABASE_NAME')
    DATABASE_PORT = os.environ.get('DATABASE_PORT', '5432')

    DNS = uri(
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        database=DATABASE_NAME,
        port=DATABASE_PORT
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup_database(DNS))
