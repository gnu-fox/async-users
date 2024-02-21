import pytest

from src.auth.models.security import Security, SecretStr

def test_security():
    password = "password"
    hashed_password = Security.hash(password)
    assert Security.verify(password, hashed_password) == True
    assert Security.verify(SecretStr(password), hashed_password) == True
