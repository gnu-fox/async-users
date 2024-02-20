import pytest
import asyncio
from datetime import timedelta, datetime
from uuid import uuid4
from jose import jwt
from jose import ExpiredSignatureError
from src.users.tokens import Claim, Token, Tokenizer


def test_token():
    sub = uuid4()
    claim1 = Claim(sub=sub, exp=timedelta(seconds=1))
    claim2 = Claim(sub=str(sub), exp=datetime.now() + timedelta(seconds=1))

    assert claim1.sub == claim2.sub
    assert claim1.exp == claim2.exp
    
    token = Tokenizer.encode(claim1)
    decoded = Tokenizer.decode(token)
    assert decoded['sub'] == str(sub)

    with pytest.raises(ExpiredSignatureError):
        asyncio.run(asyncio.sleep(2))
        Tokenizer.decode(token)

    
    