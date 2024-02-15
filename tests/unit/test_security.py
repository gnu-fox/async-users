import pytest
from uuid import uuid4

from src.auth.models import Security
from src.auth.models import Claim, Token, Tokenizer

def test_hash():
    password = "password"
    hashed = Security.hash(password)
    assert Security.verify(password, hashed)

def test_encode():
    account = uuid4()
    claim = Claim(sub=account)
    token = Tokenizer.encode(claim=claim)
    assert token.access_token
    assert token.token_type == "bearer"