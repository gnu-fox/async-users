import pytest

from passlib.context import CryptContext
from pydantic import SecretStr

from src.users.security import Security

def test_security():
    context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    pwd = 'password'
    hash = context.hash(pwd)
    assert context.verify(pwd, hash)

    security = Security()

    pwd = SecretStr('password')

    hash = security.hash(pwd)
    assert security.verify(pwd, hash)
