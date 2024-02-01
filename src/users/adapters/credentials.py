from uuid import uuid4
from typing import Union

from sqlalchemy import insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.ddd.ports import DataAccessObject as DAO
from src.users.adapters.schemas import Account as Schema
from src.users.domain.models import ID
from src.users.domain.services import Security

class Credentials(DAO):
    def __init__(self, session : AsyncSession = None):
        self.session = session

    async def verify(self, id : ID, password : str)->bool:
        statement = select(Schema).where(Schema.id == id)
        result = await self.session.execute(statement)
        schema = result.scalars().first()
        if not schema:
            return False
        return Security.verify(password, schema.password)
    

    async def update(self, id : ID, password : str) -> bool:
        hash = Security.hash(password)
        statement = update(Schema).where(Schema.id == id).values(password=hash)
        await self.session.execute(statement)