import socket
from typing import Union

from sqlalchemy import URL
from pydantic import Field
from pydantic import SecretStr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: Union[str, URL]

DEFAULT_DATABASE_URL = URL.create(
    drivername = 'postgresql+asyncpg',
    username = 'postgres',
    password = 'postgres',
    host = socket.gethostbyname('postgres'),
    port = 5432,
    database = 'postgres'
)

DEFAULT_SETTINGS = Settings(
    database_url = DEFAULT_DATABASE_URL
)