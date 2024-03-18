
from typing import List
from models.models import Product
from routers.schemas import ProductRequest
from uuid import UUID
import abc


class IProductService(abc.ABC):

    @abc.abstractmethod
    async def all(offset: int, limit: int) -> List[Product]:
        raise NotImplementedError

    @abc.abstractmethod
    async def one(id: UUID):
        raise NotImplementedError

    @abc.abstractmethod
    async def create(product: ProductRequest):
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(id: UUID):
        raise NotImplementedError

    @abc.abstractmethod
    async def update_stock(id: UUID, stock: int):
        raise NotImplementedError
