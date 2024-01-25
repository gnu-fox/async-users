from uuid import uuid4
from typing import Union

from sqlalchemy import select, insert, update, delete
from sqlalchemy import URL
from sqlalchemy.engine import Engine, create_engine

from sqlalchemy.orm import Session, sessionmaker
from passlib.context import CryptContext

from src.auth.domain.models import SecretStr, ID
from src.auth.domain.aggregates import Account
from src.auth.ports.repository import Accounts as CRUD
from src.auth.adapters.sqlalchemy.schemas import Account as Schema

cryptography = CryptContext(schemes=["bcrypt"], deprecated="auto")

class ORM:
    def __init__(self, url: Union[str, URL]):
        self.engine = create_engine(url=url)
        self.session_factory = sessionmaker(bind=self.engine)
        self.session = None

    def __enter__(self):
        self.session = self.session_factory()
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            if exc_type is None:
                self.session.commit()
            else:
                self.session.rollback()
        finally:
            self.session.close()


class Accounts(CRUD):

    def __init__(self, url : Union[str, URL]):
        pass
    
    def create(self, username : str, password : SecretStr):
        with ORM()
        hash = cryptography.hash(password.get_secret_value())
        self.session.execute(
            insert(Schema).values(id=uuid4(), username=username, password=hash)
        )

    def read(self, **kwargs) -> Union[Account, None]:
        key, value = kwargs.popitem()
        schema = self.session.execute(
            select(Schema).where(getattr(Schema, key) == value)
        ).scalar_one_or_none()
        
        if schema:
            account = Account(id=schema.id, username=schema.username)
            account.verify = lambda password : cryptography.verify(password.get_secret_value(), schema.password)
            return account
        return None

    def delete(self, id : ID):
        self.session.execute(
            delete(Schema).where(Schema.id == id)
        )