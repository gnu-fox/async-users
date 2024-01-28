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


class Security:
    context : Cryptography = CryptContext(schemes=['sha256_crypt'], deprecated='auto')

    def __init___(self, hash : Union[str, SecretStr]):  
        self.verify = lambda secret : self.context.verify(reveal(secret), hash)

    @classmethod
    def hash(cls, password : Union[str, SecretStr]) -> str:
        return cls.context.hash(reveal(password))