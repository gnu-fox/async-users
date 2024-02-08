from typing import Union
from typing import List
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from passlib.context import CryptContext

from pydantic import Field
from pydantic_settings import BaseSettings

from src.auth.protocols import Cryptography

class Settings(BaseSettings):
    database_uri : Union[URL, str, None]
    security_schemes : List[str] = ['bcrypt']




