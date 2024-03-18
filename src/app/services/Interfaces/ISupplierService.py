
from typing import List
from models.models import Supplier
from uuid import UUID
from routers.schemas import SupplierRequest, AddressRequest
import abc


class ISupplierService(abc.ABC):

    @abc.abstractmethod
    async def all(offset: int, limit: int) -> List[Supplier]:
        raise NotImplementedError

    @abc.abstractmethod
    async def one(id: UUID) -> Supplier:
        raise NotImplementedError

    @abc.abstractmethod
    async def create(supplier: SupplierRequest):
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(id: UUID):
        raise NotImplementedError

    @abc.abstractmethod
    async def update_address(id: UUID, address: AddressRequest) -> Supplier:
        raise NotImplementedError
