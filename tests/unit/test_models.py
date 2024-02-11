import pytest
from uuid import uuid4
from uuid import UUID

from src.domain.messages import Event
from src.domain.models import Account
from src.domain.models import User
from src.domain.models import Credentials
from src.domain.services import Security

class SomeEvent(Event):
    pass

def test_accounts():
    account_uuid = uuid4()
    account1 = Account(id = account_uuid)
    assert isinstance(account1.id,UUID)
    account2 = Account(id = account_uuid)
    assert isinstance(account2.id, UUID)
    assert account1 == account2

def test_users():
    account_uuid = uuid4()
    account1 = Account(id = account_uuid)
    user1 = User(account1)
    account2 = Account(id = account_uuid)
    user2 = User(account2)
    assert user1 == user2
    assert user1 != account1
    assert user1 != account2

    user1.events.append(SomeEvent())
    event = user1.events.pop()
    assert isinstance(event, SomeEvent)

def test_credentials():
    credentials = Credentials(username='test', password='test')
    assert credentials.password.get_secret_value() != 'test'
    assert credentials.verify('test')
    assert credentials.verify(None) == False

    credentials = Credentials(username='test_withouth_password')
    assert credentials.verify('test') == False
