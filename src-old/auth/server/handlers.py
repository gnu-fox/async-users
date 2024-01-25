from src.auth.ports.context import Users

from src.auth.domain.commands import (
    Command,
    Authenticate,
    Register
)

from src.auth.domain.events import (
    Event,
    Authenticated
)


def handle_authenticate(command : Command[Authenticate], users : Users):
    username = command.payload.username
    password = command.payload.password
    with users:
        users.accounts.authenticate()
