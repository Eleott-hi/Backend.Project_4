
from typing import Optional, List, Any
from models.models import Address, Client
from repositories.Interfaces.IClientRepository import IClientRepository
from services.Interfaces.IClientService import IClientService
from uuid import UUID
from routers.schemas import ClientRequest, AddressRequest
from fastapi import HTTPException


class ClientService(IClientService):

    def __init__(self, repository: IClientRepository) -> None:
        self.repository = repository

    async def all(self, name: Optional[str], surname: Optional[str], offset: int, limit: int) -> List[Client]:
        res = await self.repository.all(name, surname, offset, limit)
        return res

    async def one(self, id: UUID) -> Client:
        res = await self.repository.one(id)
        return res

    async def create(self, client: ClientRequest) -> Client:
        client = self.__mapping(client, Client)
        res = await self.repository.create(client)
        return res

    async def update_address(self, id: UUID, address: AddressRequest) -> Client:
        address = self.__mapping(address, Address)
        res = await self.repository.update_address(id, address)
        return res

    async def delete(self, id: UUID) -> str:
        res = await self.repository.delete(id)
        return res

    def __mapping(self, obj: Any, obj_cls: type) -> Client:
        try:
            return obj_cls.model_validate(obj)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
