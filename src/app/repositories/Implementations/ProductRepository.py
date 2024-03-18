from typing import List
from models.models import Product, Supplier
from sqlmodel import select, Session
from database.database import engine
from fastapi.exceptions import HTTPException
from uuid import UUID
from repositories.Interfaces.IProductRepository import IProductRepository


class ProductRepository(IProductRepository):

    async def all(self, offset: int, limit: int) -> List[Product]:
        with Session(engine) as session:
            query = select(Product)
            query = query.offset(offset).limit(limit)
            res = session.exec(query).all()

            return res

    async def one(self, id: UUID) -> Product:
        with Session(engine) as session:
            product = self.__get_or_404(Product, id, session=session)

            return product

    async def create(self, product: Product) -> Product:
        with Session(engine) as session:
            if product.supplier_id:
                supplier = self.__get_or_404(
                    Supplier, product.supplier_id, "Supplier not found", session=session
                )

            session.add(product)
            session.commit()
            session.refresh(product)

            return product

    async def delete(self, id: UUID) -> str:
        with Session(engine) as session:
            product = self.__get_or_404(Product, id, session=session)
            session.delete(product)
            session.commit()

            return "Product deleted successfully"

    async def update_stock(self, id: UUID, stock: int) -> Product:
        with Session(engine) as session:
            product = self.__get_or_404(Product, id, session=session)

            product.available_stock = stock
            session.add(product)
            session.commit()
            session.refresh(product)

            return product

    def __get_or_404(self, cls: type, id: UUID, detail: str = "Product not found", session: Session = None):
        item = session.get(cls, id)
        if not item:
            raise HTTPException(status_code=404, detail=detail)

        return item
