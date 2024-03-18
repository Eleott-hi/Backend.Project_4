from typing import Optional, List
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship
from datetime import date, datetime
from enum import Enum

from pydantic_extra_types.phone_numbers import PhoneNumber


class Address(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    country: str
    city: str
    street: str

    clients: List["Client"] = Relationship(back_populates="address")
    suppliers: List["Supplier"] = Relationship(back_populates="address")


class Supplier(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str
    phone_number: PhoneNumber
    address_id: Optional[UUID] = Field(default=None, foreign_key="address.id")

    address: Optional[Address] = Relationship(back_populates="suppliers")
    products: list["Product"] = Relationship(
        back_populates="supplier", sa_relationship_kwargs={"cascade": "delete"}
    )


class Image(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    image: bytes

    product: Optional["Product"] = Relationship(back_populates="image")


class Product(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str
    category: str
    price: float
    available_stock: int
    last_update_date: datetime = Field(default=datetime.now())
    supplier_id: Optional[UUID] = Field(default=None, foreign_key="supplier.id")
    image_id: Optional[UUID] = Field(default=None, foreign_key="image.id")

    image: Optional[Image] = Relationship(back_populates="product")
    supplier: Optional[Supplier] = Relationship(back_populates="products")


class Sex(str, Enum):
    male = "male"
    female = "female"


class Client(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    client_name: str
    client_surname: str
    birthday: date
    gender: Sex
    registration_date: datetime = Field(default=datetime.now())
    address_id: Optional[UUID] = Field(default=None, foreign_key="address.id")

    address: Optional[Address] = Relationship(back_populates="clients")
