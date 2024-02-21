from typing import Union

from sqlalchemy import URL
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_uri : Union[str, URL]    
    token_url : str = "/token"