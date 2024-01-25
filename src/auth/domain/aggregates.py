from uuid import UUID
from typing import Union

ID = Union[str, UUID]

class Account:
    def __init__(self, id : ID, username : str):
        self.id = id
        self.username = username