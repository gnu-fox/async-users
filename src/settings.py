from typing import Union

from sqlalchemy import URL
from pydantic import Field
from pydantic import SecretStr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: Union[str, URL]
