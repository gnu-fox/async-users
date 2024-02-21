from typing import Protocol
from typing import Any
from dataclasses import dataclass

@dataclass
class Account:
    id : Any

class User:
    def __init__(self, account : Account):
        self.__id = account.id

    @property
    def id(self):
        return self.__id
    
    def __eq__(self, __value: object) -> bool:
        return self.id == __value.id if isinstance(__value, self.__class__) else False
    
    def __hash__(self) -> int:
        return hash(self.id)