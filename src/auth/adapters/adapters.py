from uuid import uuid4
from uuid import UUID
from typing import Optional
from typing import Union
from typing import Any

from sqlalchemy import URL
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.adapters.schemas import ACCOUNT
from src.auth.models.credentials import Credentials
from src.auth.models.accounts import Account

class Accounts:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, account : Account):
        credentials = account.credentials
        if credentials.username and credentials.password:
            command = insert(ACCOUNT).values(id=account.id, **credentials.model_dump(exclude_none=True))
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
            credentials = Credentials(
                username=account.username, 
                password=account.password)
            return Account(id=account.id, credentials=credentials)

    async def update(self, account : Account):
        command = update(ACCOUNT).where(ACCOUNT.id == account.id).values(**account.credentials.model_dump(exclude_none=True))
        await self.session.execute(command)

    async def delete(self, account : Account):
        command = delete(ACCOUNT).where(ACCOUNT.id == account.id)
        await self.session.execute(command)


class SessionFactory:
    def __init__(self, url : Union[str, URL]):
        self.engine = create_async_engine(url=url)
        self.session_factory = async_sessionmaker(self.engine, class_=AsyncSession)

    def __call__(self) -> AsyncSession:
        return self.session_factory()    


class UnitOfWork:
    def __init__(self, session_factory : SessionFactory):
        self.session_factory = session_factory

    async def begin(self):
        self.session = self.session_factory()
        self.accounts = Accounts(session=self.session)
        await self.session.begin()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def close(self):
        await self.session.close()

    async def __aenter__(self):
        await self.begin()
        return self
    
    async def __aexit__(self, exc_type : Any, exc_value : Any, traceback : Any):
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()
        await self.close()