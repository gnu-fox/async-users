from uuid import uuid4
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

class Event(BaseModel):
    id : UUID = Field(default_factory=uuid4)
    timestamp : datetime = Field(default_factory=datetime.now)
    model_config = ConfigDict(frozen=True)