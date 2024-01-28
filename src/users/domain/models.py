from uuid import UUID
from typing import Union

from pydantic import BaseModel, SecretStr

from src.users.domain.services import Security

ID = Union[str, UUID]

class Account(BaseModel):
    id : ID
    username : str
    security : Security
    
    class Config:
        arbitrary_types_allowed = True

        