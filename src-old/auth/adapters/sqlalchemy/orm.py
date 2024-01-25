from typing import Union, List

from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker, Session

from auth.adapters.sqlalchemy.crud import CRUD, Accounts

class ORM:
    def __init__(self, url : Union[str, URL]):
        self.engine = create_engine(url=url)
        self.session_factory = sessionmaker(bind=self.engine, autocommit=False, autoflush=False)
        self.accounts = Accounts(session=None)
        
        self.repositories = [self.accounts]

    @property
    def session(self) -> Session:
        session = self.session_factory()
        for repository in self.repositories:
            repository.__init__(session=session)
        return session