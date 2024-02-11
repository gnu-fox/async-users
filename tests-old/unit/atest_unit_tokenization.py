import pytest
from uuid import uuid4
from datetime import timedelta

from src.auth.security import Token, JWT

@pytest.fixture
def tokenizer():
    return JWT()

def test_encode_decode(tokenizer : JWT):
    subject = uuid4()
    token = tokenizer.encode(subject)
    decoded_token = tokenizer.decode(token)
    assert decoded_token["subject"] == str(subject)

def test_expired_token(tokenizer : JWT):
    token = tokenizer.encode("user@example.com", expires_delta=timedelta(seconds=1))

    import time
    time.sleep(2)

    with pytest.raises(ValueError) as excinfo:
        tokenizer.decode(token)

    assert "Token has expired" in str(excinfo.value)

def test_invalid_token(tokenizer : JWT):
    invalid_token = Token(access_token="invalid_token")
    
    with pytest.raises(ValueError) as excinfo:
        tokenizer.decode(invalid_token)

    assert "Invalid token" in str(excinfo.value)