from uuid import UUID
import abc


class IImageService(abc.ABC):

    @abc.abstractmethod
    async def one(id: UUID) -> bytes:
        raise NotImplementedError

    @abc.abstractmethod
    async def one_by_product_id(product_id: UUID):
        raise NotImplementedError

    @abc.abstractmethod
    async def create(image: bytes, product_id: UUID):
        raise NotImplementedError

    @abc.abstractmethod
    async def update(id: UUID, image: bytes):
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(id: UUID):
        raise NotImplementedError
