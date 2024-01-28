from uuid import uuid4
from typing import Union

from sqlalchemy import insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.adapters.schemas import Account as Schema
from src.users.domain.models import ID, Account, SecretStr
from src.users.domain.services import Security

class Accounts:
    def __init__(self, session : AsyncSession):
        self.__session = session

    async def create(self, username : str, password : Union[str, SecretStr]):
        statement = select(Schema).where(Schema.username == username)
        result = await self.__session.execute(statement)
        schema = result.scalars().first()
        if schema:
            raise Exception(f'Account with username {username} already exists')

        hash = Security.hash(password)
        statement = insert(Schema).values(id=uuid4(), username=username, password=hash)
        await self.__session.execute(statement)

    async def read(self, **kwargs) -> Union[Account, None]:
        key, value = kwargs.popitem()
        if key not in ['id', 'username']:
            raise KeyError(f'Invalid key {key}')

        statement = select(Schema).where(getattr(Schema, key) == value)
        result = await self.__session.execute(statement)
        schema = result.scalars().first()

        if schema:
            security = Security(schema.password)
            account = Account(id=schema.id, username=schema.username, security=security)
            return account
        return None
    
    async def delete(self, id : ID):
        statement = delete(Schema).where(Schema.id == id)
        await self.__session.execute(statement)




