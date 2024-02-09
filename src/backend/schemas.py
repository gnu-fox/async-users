from sqlalchemy.orm import declarative_base
from sqlalchemy import Column
from sqlalchemy import UUID
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import func

Schema = declarative_base()

class Account(Schema):
    __tablename__ = 'accounts'
    id = Column(UUID, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())