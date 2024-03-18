from fastapi import APIRouter, status
from typing import List
from routers.schemas import SupplierRequest, SupplierResponse, AddressRequest
from uuid import UUID
from services.Interfaces.ISupplierService import ISupplierService


class SupplierRouter():
    def __init__(self, service: ISupplierService):

        self.router = APIRouter(prefix="/suppliers", tags=["Suppliers"])
        self.service = service

        @self.router.get("/", response_model=List[SupplierResponse])
        async def get_all_suppliers(offset: int = 0, limit: int = 100) -> List[SupplierResponse]:
            """
            Retrieve a list of suppliers.

            - `offset`: Optional integer. Number of records to skip.
            - `limit`: Optional integer. Maximum number of records to retrieve.

            Returns:
            - List of `SupplierResponse` objects.
            """
            res = await self.service.all(offset, limit)
            return res

        @self.router.get("/{id}", response_model=SupplierResponse, responses={404: {"description": "Item not found"}})
        async def get_supplier_by_id(id: UUID) -> SupplierResponse:
            """
            Retrieve a supplier by its ID.

            - `id`: UUID. ID of the supplier to retrieve.

            Returns:
            - `SupplierResponse` object.
            """
            res = await self.service.one(id)
            return res

        @self.router.post("/", status_code=status.HTTP_201_CREATED, response_model=SupplierResponse)
        async def create_supplier(supplier: SupplierRequest) -> SupplierResponse:
            """
            Create a new supplier.

            - `supplier`: `SupplierRequest` object containing supplier data.

            Returns:
            - `SupplierResponse` object of the created supplier.
            """
            res = await self.service.create(supplier)
            return res

        @self.router.delete("/{id}", responses={404: {"description": "Item not found"}})
        async def delete_supplier(id: UUID) -> str:
            """
            Delete a supplier by its ID.

            - `id`: UUID. ID of the supplier to delete.

            Returns:
            - Success message.
            """
            res = await self.service.delete(id)
            return res

        @self.router.patch("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=SupplierResponse, responses={404: {"description": "Item not found"}})
        async def update_supplier_address(id: UUID, address: AddressRequest) -> SupplierResponse:
            """
            Update the address of a supplier.

            - `id`: UUID. ID of the supplier to update.
            - `address`: `AddressRequest` object containing the new address.

            Returns:
            - `SupplierResponse` object of the updated supplier.
            """
            res = await self.service.update_address(id, address)
            return res
