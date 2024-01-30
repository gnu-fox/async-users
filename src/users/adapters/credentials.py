from uuid import uuid4
from typing import Union

from sqlalchemy import insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.adapters.db_schemas import Account as Schema
from src.users.domain.models import ID, SecretStr
from src.users.domain.services import Security

from src.users.ports.utils import DataAccessObject as DAO


class Credentials(DAO):
    def __init__(self, session : AsyncSession):
        self.session = session

    async def verify(self, id : ID, password : Union[str, SecretStr])->bool:
        statement = select(Schema).where(Schema.id == id)
        result = await self.session.execute(statement)
        schema = result.scalars().first()
        if not schema:
            return False
        return Security.verify(password, schema.password)
    

    async def change_password(self, id : ID, old_password : Union[str, SecretStr], new_password : Union[str, SecretStr]) -> bool:
        verified = await self.verify(id, old_password)
        if not verified:
            return False

        hash = Security.hash(new_password)
        statement = update(Schema).where(Schema.id == id).values(password=hash)
        await self.session.execute(statement)