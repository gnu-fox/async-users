from typing import Any
from typing import Deque
from collections import deque

from pydantic import BaseModel
from pydantic import ConfigDict

from users.domain.messages import Event

ID = Any

class Entity(BaseModel):
    id : ID

    def __eq__(self, other: Any):
        if not isinstance(other, Entity):
            return False
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

class Root(Entity):
    events : Deque[Event] = deque()

class Account(Root):
    pass