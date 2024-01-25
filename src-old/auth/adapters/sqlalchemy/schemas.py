from sqlalchemy import Column, String, UUID, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Account(Base):
    __tablename__ = "accounts"

    id = Column(UUID(as_uuid=True), primary_key=True)
    username = Column(String(50), nullable = False, unique = True)
    password = Column(String(100), nullable = False)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())