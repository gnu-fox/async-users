from uuid import uuid4
from uuid import UUID
from typing import Optional

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models import Account
from src.domain.models import Credentials
from src.adapters.data_schemas import ACCOUNT

class Accounts:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, credentials : Credentials):
        if credentials.username and credentials.password:
            command = insert(ACCOUNT).values(id=uuid4(), username=credentials.username, password=credentials.password.get_secret_value())
            await self.session.execute(command)
        else:
            raise KeyError("Invalid credentials")    

    async def read(self, credentials : Credentials) -> Optional[Account]:
        if credentials.username:
            query = select(ACCOUNT).where(ACCOUNT.username == credentials.username)
        else:
            raise KeyError("Invalid credentials")
            
        result = await self.session.execute(query)
        account = result.scalars().first()
        if account:
            return Account(id=account.id)

    async def update(self, account : Account, credentials : Credentials):
        command = update(ACCOUNT).where(ACCOUNT.id == account.id).values(credentials.model_dump())
        await self.session.execute(command)

    async def delete(self, account : Account):
        command = delete(ACCOUNT).where(ACCOUNT.id == account.id)
        await self.session.execute(command)