import pytest
from uuid import uuid4
from uuid import UUID

from src.users.models import ID
from src.users.models import Account
from src.users.models import Credentials

def test_accounts():
    account_id = uuid4()
    account = Account(identity=account_id)
    assert isinstance(account.id, UUID)
    account2 = Account(identity=ID(root=account_id))
    assert isinstance(account.id, UUID)
    assert account == account2

def test_credentials():
    credentials1 = Credentials(username="pepe")
    credentials2 = Credentials(password="12sdsd2")
    credentials3 = Credentials(username="lala", password="lala")