from typing import Any, List
from models.models import Supplier, Address
from sqlmodel import select, Session
from database.database import engine
from fastapi.exceptions import HTTPException
from uuid import UUID
from repositories.Interfaces.ISupplierRepository import ISupplierRepository


class SupplierRepository(ISupplierRepository):

    async def all(self, offset: int = 0, limit: int = 100) -> List[Supplier]:
        with Session(engine) as session:

            query = select(Supplier)
            query = query.offset(offset).limit(limit)
            res = session.exec(query).all()

            return res

    async def one(self, id: UUID) -> Supplier:
        with Session(engine) as session:
            supplier = self.__get_or_404(Supplier, id, session=session)

            return supplier

    async def create(self, supplier: Supplier) -> Supplier:
        with Session(engine) as session:
            if supplier.address_id is not None:
                address = self.__get_or_404(
                    Address,
                    supplier.address_id,
                    detail="Address not found",
                    session=session,
                )

            session.add(supplier)
            session.commit()
            session.refresh(supplier)

            return supplier

    async def delete(self, id: UUID) -> str:
        with Session(engine) as session:

            supplier = self.__get_or_404(Supplier, id, session=session)
            session.delete(supplier)
            session.commit()

            return "Supplier deleted successfully"

    async def update_address(self, id: UUID, address: Address) -> Supplier:
        with Session(engine) as session:

            supplier = self.__get_or_404(Supplier, id, session=session)

            query = select(Address)
            query = query.where(Address.country == address.country)
            query = query.where(Address.city == address.city)
            query = query.where(Address.street == address.street)

            db_address = session.exec(query).one_or_none()

            if not db_address:
                session.add(address)
                session.commit()
                session.refresh(address)
                db_address = address

            supplier.address = db_address
            session.add(supplier)
            session.commit()
            session.refresh(supplier)

            return supplier

    def __get_or_404(self,  cls: type, id: UUID, detail: str = "Supplier not found", session: Session = None) -> Any:
        item = session.get(cls, id)
        if not item:
            raise HTTPException(status_code=404, detail=detail)

        return item
