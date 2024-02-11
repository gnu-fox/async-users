import pytest
from uuid import uuid4
from typing import Union
from typing import Any

from src.domain.models import Account
from src.domain.models import User
from src.domain.messages import Event, Command
from src.domain.repository import Repository
from src.domain.application import Handler, Application

class CreateAccount(Command):
    username : str
    password : str

class AccountCreated(Event):
    account_id : Any

class SendNotification(Command):
    account_id : Any
    notification : str

class PublishOnlineStatus(Command):
    pass

class NotificationSended(Event):
    status : bool = False

triggered_messages = []

class create_account(Handler[Command]):
    def __init__(self, repository : Repository):
        self.repository = repository

    async def __call__(self, command : CreateAccount):
        account = Account(id = uuid4())
        print(f"creating account with id {account.id}")
        user = User(account)
        self.repository.add(user)
        user.events.append(AccountCreated(account_id=account.id))

class account_created(Handler[Event]):    
    async def __call__(self, event : AccountCreated):
        print(f"created account {event.account_id}")

class send_notification(Handler): #[Command] not setted with testing purposes
    def __init__(self, repository : Repository):
        self.repository = repository

    async def __call__(self, command : SendNotification):
        print(f"sending notification to {command.account_id}")
        user = self.repository.get(command.account_id)
        user.events.append(NotificationSended(status=True))
        triggered_messages.append(NotificationSended(status=True))

class publish_online_status(Handler):
    async def __call__(self, command : PublishOnlineStatus):
        print("User now is online")
        triggered_messages.append(PublishOnlineStatus())

@pytest.mark.asyncio
async def test_application():
    repository = Repository()
    application = Application(repository)

    application.publishers = {
        CreateAccount : create_account(repository),
        SendNotification : send_notification(repository),
        PublishOnlineStatus : publish_online_status()
    }

    application.consumers = {
        AccountCreated : [send_notification(repository), publish_online_status()],
        NotificationSended : []
    }

    await application.handle(CreateAccount(username="test", password="password"))

    for message in triggered_messages:
        if isinstance(message, NotificationSended):
            assert message.status == True

    assert len(triggered_messages) == 2