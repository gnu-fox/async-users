from uuid import uuid4, UUID
from typing import Dict
from typing import Any
from typing import Optional

from sqlalchemy import insert, delete, select, update
from sqlalchemy import Column
from sqlalchemy import UUID
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import declarative_base
from passlib.context import CryptContext

from src.auth.ports import Security
from src.auth.settings import Settings

Schema = declarative_base()

class Credentials(Schema):
    __tablename__ = 'credentials'
    id = Column(UUID, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Accounts:
    security = Security(CryptContext(schemes = ['bcrypt'], deprecated = 'auto'))

    def __init__(self, session : AsyncSession = None):
        self.session = session
        self.security_service = self.security

    async def create(self, credentials : Dict[str, Any]) -> UUID:
        result = await self.session.execute(
            select(Credentials).where(Credentials.username == credentials['username'])
        )
        if result.scalars().first() is not None:
            raise ValueError(f"Username {credentials['username']} already exists")

        password = self.security_service.hash(credentials['password'])
        account_id = uuid4()
        await self.session.execute(
            insert(Credentials).values(id = account_id, username = credentials['username'], password = password)
        )
        return account_id
    
    
    async def verify(self, credentials : Dict[str, Any]) -> bool:
        username = credentials['username']
        password = credentials['password']
        result = await self.session.execute(
            select(Credentials).where(Credentials.username == username)
        )
        account = result.scalars().first()
        return self.security_service.verify(password, account.password) if account else False
    

    async def read(self, credentials : Dict[str, Any]) -> Optional[UUID]:
        username = credentials['username']
        result = await self.session.execute(
            select(Credentials).where(Credentials.username == username)
        )
        account = result.scalars().first()
        return account.id if account else None
    
    async def update(self, id : UUID, credentials : Dict[str, Any]):
        if credentials['password']:
            password = self.security_service.hash(credentials['password'])
            await self.session.execute(
                update(Credentials).where(Credentials.id == id).values(password = password)
            )
        
        if credentials['username']:
            await self.session.execute(
                update(Credentials).where(Credentials.id == id).values(username = credentials['username'])
            )

    async def delete(self, id : UUID):
        await self.session.execute(
            delete(Credentials).where(Credentials.id == id) 
        )


class SessionFactory:
    def __init__(self, settings : Settings):
        self.engine = create_async_engine(url = settings.database_uri)
        self.sessionmaker = async_sessionmaker(self.engine, expire_on_commit = False)

    def __call__(self) -> AsyncSession:
        return self.sessionmaker()