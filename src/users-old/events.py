from uuid import uuid4
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

class Event(BaseModel):
    model_config = ConfigDict(frozen=True)

class UserCreated(Event):
    id : UUID = Field(default_factory=uuid4, alias="id", description="The UUID of the Account")

