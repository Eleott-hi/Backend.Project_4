
from typing import List
from models.models import Product
from routers.schemas import ProductRequest
from uuid import UUID
from services.Interfaces.IProductService import IProductService
from repositories.Interfaces.IProductRepository import IProductRepository


class ProductService (IProductService):
    def __init__(self, repository: IProductRepository):
        self.repository = repository

    async def all(self, offset: int, limit: int) -> List[Product]:
        res = await self.repository.all(offset, limit)
        return res

    async def one(self, id: UUID):
        res = await self.repository.one(id)
        return res

    async def create(self, product: ProductRequest):
        product = Product.model_validate(product)
        res = await self.repository.create(product)
        return res

    async def delete(self, id: UUID):
        res = await self.repository.delete(id)
        return res

    async def update_stock(self, id: UUID, stock: int):
        res = await self.repository.update_stock(id, stock)
        return res
