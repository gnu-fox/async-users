from typing import Protocol

class Session(Protocol):

    async def begin(self):
        ...

    async def commit(self):
        ...

    async def rollback(self):
        ...

    async def close(self):
        ...