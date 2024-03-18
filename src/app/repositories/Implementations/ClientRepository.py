from typing import Optional, List, Any
from models.models import Client, Address
from sqlmodel import select, Session
from database.database import engine
from fastapi.exceptions import HTTPException
from uuid import UUID

from repositories.Interfaces.IClientRepository import IClientRepository


class ClientRepository(IClientRepository):

    def __get_or_404(self,
                     cls: type,
                     id: UUID,
                     detail: str = "Client not found",
                     session: Session = None
                     ) -> Any:
        item = session.get(cls, id)

        if not item:
            raise HTTPException(status_code=404, detail=detail)

        return item

    async def all(self,
                  name: Optional[str] = None,
                  surname: Optional[str] = None,
                  offset: int = 0,
                  limit: int = 100,
                  ) -> List[Client]:
        with Session(engine) as session:
            query = select(Client)

            if name is not None:
                query = query.where(Client.client_name == name)

            if surname is not None:
                query = query.where(Client.client_surname == surname)

            query = query.offset(offset).limit(limit)
            res = session.exec(query).all()

            return res

    async def one(self, id: UUID) -> Client:
        with Session(engine) as session:
            client = self.__get_or_404(Client, id, session=session)
            return client

    async def create(self, client: Client) -> Client:
        with Session(engine) as session:
            if client.address_id is not None:
                address = self.__get_or_404(
                    Address,
                    client.address_id,
                    detail="Address not found",
                    session=session
                )
            session.add(client)
            session.commit()
            session.refresh(client)

            return client

    async def update_address(self, id: UUID, address: Address):
        with Session(engine) as session:
            client = self.__get_or_404(Client, id, session=session)

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

            client.address = db_address
            session.add(client)
            session.commit()
            session.refresh(client)

            return client

    async def delete(self, id: UUID) -> str:
        with Session(engine) as session:
            client = self.__get_or_404(Client, id, session=session)
            session.delete(client)
            session.commit()

            return "Client deleted successfully"
