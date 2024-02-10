from typing import Any
from typing import List

from pydantic import BaseModel
from pydantic import RootModel
from pydantic import ConfigDict
from pydantic import SecretStr, EmailStr
from pydantic import Field
from pydantic.dataclasses import dataclass

class ID(RootModel):
    root : int

class Event:
    pass

class Account:
    def __init__(self, root : ID):
        self.root = root
        self.events : List[Event] = []

    @property
    def id(self):
        if isinstance(self.root, ID):
            return self.root.root
        else:
            return self.root

    def __eq__(self, other):
        if isinstance(other, Account):
            return self.id == other.id
        return False
    
    def __hash__(self):
        return hash(self.id)
    

account = Account(root=ID(1))
print(account.id)