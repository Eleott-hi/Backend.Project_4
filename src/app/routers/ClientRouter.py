from fastapi import APIRouter, status
from typing import Optional, List
from services.Interfaces.IClientService import IClientService
import routers.schemas as schemas
from uuid import UUID



class ClientRouter():
    def __init__(self, service: IClientService):
        self.router = APIRouter(prefix="/clients", tags=["Clients"])
        self.service = service

        @self.router.get("/", response_model=List[schemas.ClientResponse])
        async def all(
            name: Optional[str] = None,
            surname: Optional[str] = None,
            offset: int = 0,
            limit: int = 100,
        ) -> List[schemas.ClientResponse]:
            """
            Retrieve a list of clients.

            - `name`: Optional string. Filter clients by name.
            - `surname`: Optional string. Filter clients by surname.
            - `offset`: Optional integer. Number of records to skip.
            - `limit`: Optional integer. Maximum number of records to retrieve.

            Returns:
            - List of `ClientResponse` objects.
            """
            res = await self.service.all(name, surname, offset, limit)
            return res

        @self.router.get("/{id}", response_model=schemas.ClientResponse, responses={404: {"description": "Item not found"}})
        async def one(id: UUID) -> schemas.ClientResponse:
            """
            Retrieve a client by ID.

            - `id`: UUID. ID of the client to retrieve.

            Returns:
            - `ClientResponse` object.
            """
            res = await self.service.one(id)
            return res

        @self.router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ClientResponse)
        async def create(client: schemas.ClientRequest) -> schemas.ClientResponse:
            """
            Create a new client.

            - `client`: `ClientRequest` object containing client data.

            Returns:
            - `ClientResponse` object of the created client.
            """
            res = await self.service.create(client)
            return res

        @self.router.patch("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ClientResponse, responses={404: {"description": "Item not found"}})
        async def update_address(
            id: UUID, address: schemas.AddressRequest
        ) -> schemas.ClientResponse:
            """
            Update the address of a client.

            - `id`: UUID. ID of the client to update.
            - `address`: `AddressRequest` object containing the new address.

            Returns:
            - `ClientResponse` object of the updated client.
            """
            res = await self.service.update_address(id, address)
            return res

        @self.router.delete("/{id}", response_model=str, responses={404: {"description": "Item not found"}})
        async def delete(id: UUID) -> str:
            """
            Delete a client by ID.

            - `id`: UUID. ID of the client to delete.

            Returns:
            - Success message.
            """
            res = await self.service.delete(id)
            return res
