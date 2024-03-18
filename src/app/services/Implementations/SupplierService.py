
from typing import List
from models.models import Supplier, Address
from uuid import UUID
from routers.schemas import SupplierRequest, AddressRequest
from services.Interfaces.ISupplierService import ISupplierService
from repositories.Interfaces.ISupplierRepository import ISupplierRepository


class SupplierService (ISupplierService):

    def __init__(self, repository: ISupplierRepository):
        self.repository = repository

    async def all(self, offset: int, limit: int) -> List[Supplier]:
        res = await self.repository.all(offset, limit)
        return res

    async def one(self, id: UUID) -> Supplier:
        res = await self.repository.one(id)
        return res

    async def create(self, supplier: SupplierRequest):
        supplier = Supplier.model_validate(supplier)
        res = await self.repository.create(supplier)
        return res

    async def delete(self, id: UUID):
        res = await self.repository.delete(id)
        return res

    async def update_address(self, id: UUID, address: AddressRequest) -> Supplier:
        address = Address.model_validate(address)
        res = await self.repository.update_address(id, address)
        return res
