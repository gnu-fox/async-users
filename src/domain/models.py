from uuid import UUID
from typing import Any
from typing import Deque
from typing import Union
from typing import Optional
from collections import deque

from pydantic import RootModel
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field, SecretStr, EmailStr
from pydantic import field_validator

from src.domain.messages import Event
from src.domain.services import Security


class ID(RootModel):
    root : Any


class ValueObject(BaseModel):
    model_config = ConfigDict(frozen=True)


class Entity(BaseModel):
    id : ID

    def __eq__(self, __value: object) -> bool:
        return self.id == __value.id if isinstance(__value, self.__class__) else False
    
    def __hash__(self) -> int:
        return hash(self.id)


class Aggregate:
    def __init__(self, root : Entity):
        self.__root = root
        self.__events : Deque[Event] = deque()

    @property
    def id(self):
        if isinstance(self.__root.id, RootModel):
            return self.__root.id.root
        else:
            return self.__root.id
        
    @property
    def events(self) -> Deque[Event]:
        return self.__events

    def __eq__(self, __value: object) -> bool:
        return self.id == __value.id if isinstance(__value, self.__class__) else False
    
    def __hash__(self) -> int:
        return hash(self.id)


class Credentials(ValueObject):
    username : Optional[str] = Field(None, description='The username of the account')
    password : Optional[SecretStr] = Field(None, description='The password of the account')

    @field_validator('password', mode='before')
    @classmethod
    def secure(cls, raw : str):
        return Security.hash(password=raw)
    
    def verify(self, password : Union[str, SecretStr]) -> bool:
        return Security.verify(password, self.password)


class Account(Entity):
    id : UUID
    authenticated : bool = False
    

class User(Aggregate):
    def __init__(self, account : Account):
        super().__init__(root=account)
        self.account = account