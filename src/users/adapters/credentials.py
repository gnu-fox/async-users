from uuid import uuid4
from typing import Union

from sqlalchemy import insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.adapters.db_schemas import Account as Schema
from src.users.domain.models import ID, SecretStr
from src.users.domain.services import Security
from src.users.ports.credentials import Credentials as Repository

class Credentials(Repository):
    def __init__(self, session : AsyncSession):
        self.__session = session

    async def verify(self, username : str, password : Union[str, SecretStr])->bool:
        statement = select(Schema).where(Schema.username == username)
        result = await self.__session.execute(statement)
        schema = result.scalars().first()
        if not schema:
            return False
        return Security.verify(password, schema.password)
    

    async def update(self, username : str, password : Union[str, SecretStr], new_password : Union[str, SecretStr]) -> bool:
        verified = await self.verify(username, password)
        if not verified:
            return False

        hash = Security.hash(new_password)
        statement = update(Schema).where(Schema.username == username).values(password=hash)
        await self.__session.execute(statement)

