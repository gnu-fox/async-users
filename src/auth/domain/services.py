from typing import Protocol, Union

from pydantic import SecretStr

class Cryptography(Protocol):

    def hash(self, password : str) -> str:
        ...

    def verify(self, password : str, hash : str) -> bool:
        ...    

class Service:
    pass

class Security(Service):
    context: Cryptography

    @classmethod
    def hash(cls, password : Union[str, SecretStr]) -> str:
        if isinstance(password, SecretStr):
            password = password.get_secret_value()
        return cls.context.hash(password)
            
    @classmethod
    def verify(cls, password : Union[str, SecretStr], hash : str) -> bool:
        if isinstance(password, SecretStr):
            password = password.get_secret_value()
        return cls.context.verify(password, hash)