from typing import Annotated
from pydantic import BaseModel, model_validator, EmailStr, StringConstraints
from pydantic_extra_types.phone_numbers import PhoneNumber


class RegistrationRequest(BaseModel):
    name: Annotated[
        str, StringConstraints(strip_whitespace=True,
                               min_length=1, max_length=256)
    ]
    surname: Annotated[
        str, StringConstraints(strip_whitespace=True,
                               min_length=1, max_length=256)
    ]
    email: EmailStr
    phone_number: PhoneNumber
    password: Annotated[
        str, StringConstraints(strip_whitespace=True,
                               min_length=7, max_length=256)
    ]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John",
                "surname": "Doe",
                "email": "john.doe@example.com",
                "phone_number": "+1234567890",
                "password": "mysecretpassword"
            }
        }


class LoginRequest(BaseModel):
    email: EmailStr
    password: Annotated[
        str, StringConstraints(strip_whitespace=True,
                               min_length=7, max_length=256)
    ]

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password": "mysecretpassword"
            }
        }


class ForgotPasswordRequest(BaseModel):
    email: EmailStr

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com"
            }
        }


class ChangePasswordRequest(BaseModel):
    email: EmailStr
    old_password: Annotated[
        str, StringConstraints(strip_whitespace=True,
                               min_length=7, max_length=256)
    ]
    new_password: Annotated[
        str, StringConstraints(strip_whitespace=True,
                               min_length=7, max_length=256)
    ]

    @model_validator(mode='after')
    def check_passwords_not_match(self) -> 'ChangePasswordRequest':
        if self.old_password == self.new_password:
            raise ValueError('Passwords match')
        return self

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "old_password": "mysecretpassword",
                "new_password": "mynewsecretpassword"
            }
        }
