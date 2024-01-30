from typing import Union
from src.users.adapters.accounts import Accounts
from src.users.adapters.credentials import Credentials
from src.users.adapters.db_orm import URL, ORM

class Provider:

    def __init__(self, url : Union[str,URL]):
        self.__orm = ORM(url = url)

    @property
    def session_factory(self):
        return self.__orm.session_factory
    
    @property
    def accounts(self) -> Accounts:
        return Accounts(session = None)
    
    @property
    def credentials(self) -> Credentials:
        return Credentials(session = None)