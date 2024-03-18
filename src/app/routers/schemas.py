from typing import Optional
from uuid import UUID
from datetime import datetime, date
from pydantic import BaseModel
from pydantic_extra_types.phone_numbers import PhoneNumber
import enum

class AddressRequest(BaseModel):
    country: str
    city: str
    street: str


class AddressResponse(AddressRequest):
    id: UUID


class SupplierRequest(BaseModel):
    name: str
    phone_number: PhoneNumber
    address_id: Optional[UUID] = None


class SupplierResponse(SupplierRequest):
    id: UUID


class ProductRequest(BaseModel):
    name: str
    category: str
    price: float
    available_stock: int
    supplier_id: Optional[UUID] = None
    image_id: Optional[UUID] = None


class ProductResponse(ProductRequest):
    id: UUID
    last_update_date: datetime

class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"

class ClientRequest(BaseModel):
    client_name: str
    client_surname: str
    birthday: date
    gender: Gender
    address_id: Optional[UUID] = None


class ClientResponse(ClientRequest):
    id: UUID
    registration_date: datetime
