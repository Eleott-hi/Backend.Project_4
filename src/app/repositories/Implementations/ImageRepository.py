from models.models import Image, Product
from sqlmodel import Session
from database.database import engine
from fastapi.exceptions import HTTPException
from uuid import UUID
from repositories.Interfaces.IImageRepository import IImageRepository


class ImageRepository(IImageRepository):

    async def one(self, id: UUID) -> bytes:
        with Session(engine) as session:
            image = self.__get_or_404(Image, id, session=session)
            return image.image

    async def one_by_product_id(self, id: UUID) -> bytes:
        with Session(engine) as session:
            product = self.__get_or_404(
                Product, id, "Product not found", session=session
            )

            if product.image is None:
                raise HTTPException(
                    status_code=404, detail="Product has no image")

            return product.image.image

    async def create(self, image: Image, product_id: UUID) -> UUID:
        with Session(engine) as session:
            product = self.__get_or_404(
                Product, product_id, "Product not found", session=session
            )

            image.product = product
            session.add(image)
            session.commit()
            session.refresh(image)

            return image.id

    async def update(self, id: UUID, image_info: bytes) -> Image:
        with Session(engine) as session:
            image = self.__get_or_404(Image, id, session=session)
            image.image = image_info

            session.add(image)
            session.commit()

            return "Image updated successfully"

    async def delete(self, id: UUID) -> str:
        with Session(engine) as session:
            image = self.__get_or_404(Image, id, session=session)
            session.delete(image)
            session.commit()

            return "Image deleted successfully"

    def __get_or_404(self, cls: type, id: UUID, detail: str = "Image not found", session: Session = None):
        item = session.get(cls, id)

        if not item:
            raise HTTPException(status_code=404, detail=detail)

        return item
