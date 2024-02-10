from uuid import uuid4
from uuid import UUID
from typing import Optional

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import Account
from src.users.models import Credentials
from src.users.security import Security
from src.backend.schemas import ACCOUNT

class Accounts:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, credentials : Credentials) -> Account:
        identity = uuid4()
        if credentials.username and credentials.password:
            query = select(ACCOUNT).where(ACCOUNT.username == credentials.username)
            result = await self.session.execute(query)
            if result.scalars().first():
                raise LookupError(f"username {credentials.username} already exists")

            secret = Security.hash(credentials.password)
            command = insert(ACCOUNT).values(id=identity, username=credentials.username, password=secret)
            await self.session.execute(command)
        else:
            raise KeyError("Invalid credentials")    
        return Account(identity=identity)
    
    async def read(self, credentials : Credentials) -> Optional[Account]:
        if credentials.username:
            query = select(ACCOUNT).where(ACCOUNT.username == credentials.username)
        else:
            raise KeyError("Invalid credentials")
            
        result = await self.session.execute(query)
        account = result.scalars().first()
        if account:
            return Account(identity=account.id)
    
    async def update(self, account : Account, credentials : Credentials):
        command = update(ACCOUNT).where(ACCOUNT.id == account.id).values(credentials.model_dump())
        await self.session.execute(command)

    async def delete(self, account : Account):
        command = delete(ACCOUNT).where(ACCOUNT.id == account.id)
        await self.session.execute(command)

    async def verify(self, credentials : Credentials) -> bool:
        if credentials.username and credentials.password:
            query = select(ACCOUNT).where(ACCOUNT.username == credentials.username)
            result = await self.session.execute(query)
            schema = result.scalars().first()
            return Security.verify(credentials.password, schema.password) if schema else False
        else:
            raise KeyError("Invalid credentials")