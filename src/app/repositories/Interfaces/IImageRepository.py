import abc
from typing import List
from uuid import UUID
from models.models import Image


class IImageRepository(abc.ABC):

    @abc.abstractmethod
    async def one(id: UUID) -> bytes:
        raise NotImplementedError

    @abc.abstractmethod
    async def one_by_product_id(id: UUID) -> bytes:
        raise NotImplementedError

    @abc.abstractmethod
    async def create(image: Image, product_id: UUID) -> UUID:
        raise NotImplementedError

    @abc.abstractmethod
    async def update(id: UUID, image_info: bytes) -> Image:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(id: UUID) -> str:
        raise NotImplementedError
