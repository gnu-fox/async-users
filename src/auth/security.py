from typing import Protocol, Union

from pydantic import SecretStr
from passlib.context import CryptContext

class Cryptography(Protocol):

    def hash(self, password : str) -> str:
        ...

    def verify(self, password : str, hash : str) -> bool:
        ...        

def reveal(secret : Union[str, SecretStr]) -> str:
    if isinstance(secret, SecretStr):
        secret = secret.get_secret_value()
    return secret

DEFAULT_CRYPTOGRAPHY_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Security:
    context : Cryptography = DEFAULT_CRYPTOGRAPHY_CONTEXT

    @classmethod
    def setup(cls, context : Cryptography) -> None:
        cls.context = context

    @classmethod
    def hash(cls, password : Union[str, SecretStr]) -> str:
        return cls.context.hash(reveal(password))
    
    @classmethod
    def verify(cls, password : Union[str, SecretStr], hash : str) -> bool:
        return cls.context.verify(reveal(password), hash)