from typing import List
from models.models import Supplier, Address
from uuid import UUID
import abc


class ISupplierRepository(abc.ABC):

    @abc.abstractmethod
    async def all(offset: int = 0, limit: int = 100) -> List[Supplier]:
        raise NotImplementedError

    @abc.abstractmethod
    async def one(id: UUID) -> Supplier:
        raise NotImplementedError

    @abc.abstractmethod
    async def create(supplier: Supplier) -> Supplier:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(id: UUID) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    async def update_address(id: UUID, address: Address) -> Supplier:
        raise NotImplementedError
