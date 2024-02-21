from pydantic.dataclasses import dataclass
from pydantic import BaseModel


class Model(BaseModel):
    id: int

class Data(BaseModel):
    id: int

data = Data(id=1)

#model_from data
model = Model(**data.dict())