import abc
from typing import Optional
from uuid import UUID
from routers.schemas import ClientRequest, AddressRequest


class IClientService(abc.ABC):

    @abc.abstractmethod
    async def all(self, name: Optional[str], surname: Optional[str], offset: int, limit: int):
        raise NotImplementedError

    @abc.abstractmethod
    async def one(self, id: UUID):
        raise NotImplementedError

    @abc.abstractmethod
    async def create(self, client: ClientRequest):
        raise NotImplementedError

    @abc.abstractmethod
    async def update_address(self, id: UUID, address: AddressRequest):
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, id: UUID):
        raise NotImplementedError
