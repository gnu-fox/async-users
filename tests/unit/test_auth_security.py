import pytest
from passlib.context import CryptContext

from src.auth.settings import Settings
from src.auth.ports import Security

def test_security():
    security = Security(context=CryptContext(
        schemes = ['bcrypt'],
        deprecated = 'auto'
    ))
    hashed_password = security.hash("password")
    assert security.verify("password", hashed_password) == True