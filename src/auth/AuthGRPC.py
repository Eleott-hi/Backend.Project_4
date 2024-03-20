import grpc
import auth_pb2
from typing import Annotated
import auth_pb2_grpc
from passlib.context import CryptContext
from passlib.pwd import genword
from database.Models.User import User
from database.database import engine
from sqlmodel import Session, select
from pydantic import BaseModel, field_validator, EmailStr, StringConstraints
from pydantic_extra_types.phone_numbers import PhoneNumber
import jwt
from datetime import datetime, timedelta


SECRET_KEY = "secret_key"
HASH_ALG = "HS256"


class RegistrationRequest(BaseModel):
    name: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=256)
    ]
    surname: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=256)
    ]
    email: EmailStr
    phone_number: PhoneNumber
    password: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=7, max_length=256)
    ]


class LoginRequest(BaseModel):
    email: EmailStr
    password: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=7, max_length=256)
    ]


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ChangePasswordRequest(BaseModel):
    email: EmailStr
    old_password: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=7, max_length=256)
    ]
    new_password: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=7, max_length=256)
    ]

    @field_validator("new_password")
    def passwords_must_be_different(cls, new_password, values):
        if "old_password" in values and new_password == values["old_password"]:
            raise ValueError("New password must be different from the old password")
        return new_password


class AuthenticationServicer(auth_pb2_grpc.AuthenticationServicer):
    def __init__(self) -> None:
        super().__init__()
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def VerifyJWT(self, request: auth_pb2.VerifyJWTRequest, context):
        self.__verify_jwt(request.token)
        return auth_pb2.EmptyResponse()

    def Login(self, request: auth_pb2.LoginRequest, context):
        request = LoginRequest(email=request.email, password=request.password)

        with Session(engine) as session:
            user = session.exec(select(User).where(User.email == request.email)).first()

            if user is None:
                raise grpc.RpcError("User with such email has no been registered")

            verified = self.pwd_context.verify(request.password, user.password_token)
            if not verified:
                raise grpc.RpcError("Email or password is not exist")

        return auth_pb2.LoginResponse(token=self.__get_jwt())

    def Registration(self, request: auth_pb2.RegistrationRequest, context):
        request = RegistrationRequest(
            name=request.name,
            surname=request.surname,
            email=request.email,
            phone_number=request.phone_number,
            password=request.password,
        )

        with Session(engine) as session:
            user = session.exec(select(User).where(User.email == request.email)).all()

            if len(user) != 0:
                raise ValueError("A user with such email already exists")

            user = User(
                name=request.name,
                surname=request.surname,
                email=request.email,
                phone_number=request.phone_number,
                password_token=self.pwd_context.hash(request.password),
            )

            session.add(user)
            session.commit()
            session.refresh(user)

        return auth_pb2.RegistrationResponse(token=self.__get_jwt())

    def ForgotPassword(self, request: auth_pb2.ForgotPasswordRequest, context):
        request = ForgotPasswordRequest(email=request.email)

        with Session(engine) as session:
            user = session.exec(select(User).where(User.email == request.email)).first()
            if user is None:
                raise ValueError("User with such email has no been registered")

            password = genword()
            user.password_token = self.pwd_context.hash(password)
            session.add(user)
            session.commit()
            session.refresh(user)

            print(
                "\n\n", "New user passwod send to email:", password, "\n\n", flush=True
            )

        return auth_pb2.EmptyResponse()

    def ChangePassword(self, request: auth_pb2.ChangePasswordRequest, context):
        request = ChangePasswordRequest(
            email=request.email,
            old_password=request.old_password,
            new_password=request.new_password,
        )

        with Session(engine) as session:
            user = session.exec(select(User).where(User.email == request.email)).first()

            if not self.pwd_context.verify(request.old_password, user.password_token):
                raise ValueError("Invalid password")

            user.password_token = self.pwd_context.hash(request.new_password)

            session.add(user)
            session.commit()
            session.refresh(user)

        return auth_pb2.EmptyResponse()

    def __get_jwt(self):
        return jwt.encode(
            {
                "role": "user",
                "expose_time": (datetime.now() + timedelta(minutes=15)).isoformat(),
            },
            SECRET_KEY,
            algorithm=HASH_ALG,
        )

    def __verify_jwt(self, encoded_jwt):
        payload = jwt.decode(encoded_jwt, SECRET_KEY, algorithms=[HASH_ALG])

        if datetime.fromisoformat(payload["expose_time"]) < datetime.now():
            raise ValueError("Exposure time is out ")
