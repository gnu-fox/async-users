from uuid import uuid4
from typing import Union
from typing import Protocol

from sqlalchemy import URL
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.auth.domain.models import SecretStr
from src.auth.domain.aggregates import Account, ID
from src.auth.domain.services import Security
from src.auth.ports.repositories import Accounts as Repository
from src.auth.adapters.schemas import Account as Schema

class Accounts(Repository):
    def __init__(self, session : AsyncSession):
        self.session = session

    async def create(self, username : str, password : Union[str, SecretStr]):
        hash = Security.hash(password)
        statement = insert(Schema).values(id=uuid4(), username=username, password=hash)
        await self.session.execute(statement)                

    async def read(self, **kwargs) -> Account:
        statement = select(Schema).filter_by(**kwargs)
        result = await self.session.execute(statement)
        schema = result.scalars().first()
        assert schema, 'Account not found'

        account = Account(id=schema.id, username=schema.username)
        return account
    
    async def delete(self, id : ID):
        statement = delete(Schema).filter_by(id=id)
        await self.session.execute(statement)