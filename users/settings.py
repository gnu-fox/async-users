from typing import Union

from pydantic_settings import BaseSettings

from users.adapters.repository import URL

class Settings(BaseSettings):
    database_url : Union[str, URL]
    