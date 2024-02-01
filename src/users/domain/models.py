from typing import TypeVar
from typing import Deque
from collections import deque

from src.ddd.domain import Entity, Aggregate, Event

from pydantic import BaseModel, Field

class Account(Entity):
    username : str = Field(..., title="username", description="username of the account")

class User(Aggregate):
    def __init__(self, account : Account):
        super().__init__(account)
        self.account = account

    @property
    def username(self):
        return self.account.username
    
    def verify(self, password : str):
        status = self.account.verify(password)
 ... to fix
        event = Event(
            payload = {
                "id" : self.id,
                "status" : status
            }

            type = "user-verified"
        )

        self.events.append(Event())

        









