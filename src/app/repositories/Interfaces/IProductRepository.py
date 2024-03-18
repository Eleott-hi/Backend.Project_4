from typing import List
from uuid import UUID
from models.models import Product
import abc


class IProductRepository(abc.ABC):
    @abc.abstractmethod
    async def all(offset: int, limit: int) -> List[Product]:
        raise NotImplementedError

    @abc.abstractmethod
    async def one(id: UUID) -> Product:
        raise NotImplementedError

    @abc.abstractmethod
    async def create(product: Product) -> Product:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(id: UUID) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    async def update_stock(id: UUID, stock: int) -> Product:
        raise NotImplementedError
