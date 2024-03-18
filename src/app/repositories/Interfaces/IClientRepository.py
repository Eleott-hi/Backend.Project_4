import abc
from typing import Optional, List
from uuid import UUID
from models.models import Client, Address

class IClientRepository(abc.ABC):

    @abc.abstractmethod
    async def all(self, name: Optional[str], surname: Optional[str], offset: int, limit: int) -> List[Client]:
        raise NotImplementedError

    @abc.abstractmethod
    async def one(self, id: UUID):
        raise NotImplementedError

    @abc.abstractmethod
    async def create(self, client: Client):
        raise NotImplementedError

    @abc.abstractmethod
    async def update_address(self, id: UUID, address: Address):
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, id: UUID):
        raise NotImplementedError
