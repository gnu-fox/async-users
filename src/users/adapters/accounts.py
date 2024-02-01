from uuid import uuid4
from typing import Union, Optional

from sqlalchemy import insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.ddd.ports import DataAccessObject as DAO
from src.users.adapters.schemas import Account as Schema
from src.users.domain.models import ID, Account
from src.users.domain.services import Security

class Accounts(DAO):
    def __init__(self, session : AsyncSession = None):
        self.session = session


    async def create(self, username : str, password : str, id : ID = None) -> Account:
        statement = select(Schema).where(Schema.username == username)
        result = await self.session.execute(statement)
        schema = result.scalars().first()
        if schema:
            raise Exception(f'Account with username {username} already exists')

        hash = Security.hash(password)
        
        if not id:
            id = uuid4()

        statement = insert(Schema).values(id=uuid4(), username=username, password=hash)
        await self.session.execute(statement)
        return Account(id=id, username=username)


    async def read(self, **kwargs) -> Optional[Account]:
        key, value = kwargs.popitem()

        if key not in ['id', 'username']:
            raise KeyError(f'Invalid key {key}')

        statement = select(Schema).where(getattr(Schema, key) == value)
        result = await self.session.execute(statement)
        schema = result.scalars().first()

        return Account(id=schema.id, username=schema.username) if schema else None
    

    async def update(self, id : ID, username : str) -> Account:
        statement = select(Schema).where(Schema.id == id)
        result = await self.session.execute(statement)
        schema = result.scalars().first()
        if not schema:
            raise Exception(f'Account with id {id} does not exist')
        
        statement = update(Schema).where(Schema.id == id).values(username=username)
        await self.session.execute(statement)
        return Account(id=id, username=username)


    async def delete(self, id : ID):
        statement = delete(Schema).where(Schema.id == id)
        await self.session.execute(statement)