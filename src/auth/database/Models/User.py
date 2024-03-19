from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from datetime import date, datetime
from enum import Enum
from pydantic_extra_types.phone_numbers import PhoneNumber


class User(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str
    surname: str
    email: str
    password_token: str
    phone_number: str
