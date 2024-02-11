import pytest
from uuid import uuid4

from src.domain.models import Account
from src.domain.models import User
from src.domain.models import Event
from src.domain.repository import Repository

def test_repository():
    account = Account(id=uuid4())
    user = User(account)
    repository = Repository()
    repository.add(user)

    user.events.append(Event())
    event_appended = False
    for event in user.events:
        assert isinstance(event, Event)
        if event:
            event_appended = True

    assert event_appended

    repository.remove(user)