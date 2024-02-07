import pytest

from uuid import uuid4
from uuid import UUID
import pydantic

from src.auth.models import ID, Account

@pytest.fixture
def account_id() -> UUID:
    return uuid4()

def test_models(account_id : UUID):
    account = Account(id = account_id)
    assert isinstance(account.id, ID)
    assert account.id.root == account_id
