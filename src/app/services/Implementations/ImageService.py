from models.models import Image
from uuid import UUID
from services.Interfaces.IImageService import IImageService
from repositories.Interfaces.IImageRepository import IImageRepository


class ImageService(IImageService):

    def __init__(self, repository: IImageRepository):
        self.repository = repository

    async def one(self, id: UUID) -> bytes:
        res = await self.repository.one(id)
        return res

    async def one_by_product_id(self, product_id: UUID):
        res = await self.repository.one_by_product_id(product_id)
        return res

    async def create(self, image: bytes, product_id: UUID):
        image = Image(image=image)
        res = await self.repository.create(image, product_id)
        return res

    async def update(self, id: UUID, image: bytes):
        res = await self.repository.update(id, image)
        return res

    async def delete(self, id: UUID):
        res = await self.repository.delete(id)
        return res
