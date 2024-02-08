from sqlalchemy import Column
from sqlalchemy import UUID
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy.orm import declarative_base

Schema = declarative_base()

class Account(Schema):
    __tablename__ = 'accounts'

    id = Column(UUID, primary_key = True)
    username = Column(String, unique=True)
    password = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())