from uuid import UUID
from typing import Union

from pydantic import BaseModel, SecretStr

ID = Union[str, UUID]

class Account(BaseModel):
    id : ID
    username : str

class User:
    pass