import pytest

from uuid import uuid4
from uuid import UUID
import pydantic

from src.auth.models import Account

@pytest.fixture
def account_id() -> UUID:
    return uuid4()

def test_models(account_id : UUID):
    account = Account(root = account_id)
    assert account.root == account_id
