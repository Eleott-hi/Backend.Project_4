import grpc
import auth_pb2
import auth_pb2_grpc
from pwd_context import PWDContext
from database.Models.User import User
from database.database import engine
from sqlmodel import Session, select
from converter import Converter
import schemas
from JWT import JWT


class AuthenticationServicer(auth_pb2_grpc.AuthenticationServicer):
    def __init__(self) -> None:
        super().__init__()
        self.pwd_context = PWDContext()
        self.converter = Converter()
        self.jwt = JWT()

    def VerifyJWT(self, request: auth_pb2.VerifyJWTRequest, context):
        self.jwt.verify_token(request.token)
        return auth_pb2.EmptyResponse()

    def Login(self, request: auth_pb2.LoginRequest, context):
        try:
            request = self.converter.convert_to(request, schemas.LoginRequest)

            with Session(engine) as session:
                user = session.exec(select(User).where(
                    User.email == request.email)).first()

                if user is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("User not found")
                    return auth_pb2.LoginResponse()

                verified = self.pwd_context.verify(
                    request.password, user.password_token)

                if not verified:
                    context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                    context.set_details("Invalid password")
                    return auth_pb2.LoginResponse()

            return auth_pb2.LoginResponse(token=self.jwt.get_token())

        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return auth_pb2.LoginResponse()

    def Registration(self, request: auth_pb2.RegistrationRequest, context):
        try:
            request = self.converter.convert_to(
                request, schemas.RegistrationRequest)

            with Session(engine) as session:
                user = session.exec(select(User).where(
                    User.email == request.email)).first()

                if user is not None:
                    context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                    context.set_details(
                        "A user with such email already exists")
                    return auth_pb2.RegistrationResponse()

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

            return auth_pb2.RegistrationResponse(token=self.jwt.get_token())

        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return auth_pb2.RegistrationResponse()

    def ForgotPassword(self, request: auth_pb2.ForgotPasswordRequest, context):
        try:
            request = self.converter.convert_to(
                request, schemas.ForgotPasswordRequest)

            with Session(engine) as session:
                user = session.exec(select(User).where(
                    User.email == request.email)).first()

                if user is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("User not found")
                    return auth_pb2.EmptyResponse()

                password = self.pwd_context.gen_password()
                user.password_token = self.pwd_context.hash(password)
                session.add(user)
                session.commit()
                session.refresh(user)

                print(
                    f"\n\n\tNew user passwod send to email: {password}\n\n",
                    flush=True
                )

            return auth_pb2.EmptyResponse()

        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return auth_pb2.RegistrationResponse()

    def ChangePassword(self, request: auth_pb2.ChangePasswordRequest, context):
        try:
            request = self.converter.convert_to(
                request, schemas.ChangePasswordRequest
            )

            with Session(engine) as session:
                user = session.exec(select(User).where(
                    User.email == request.email)).first()

                if not self.pwd_context.verify(request.old_password, user.password_token):
                    context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                    context.set_details("Invalid password")
                    return auth_pb2.EmptyResponse()

                user.password_token = self.pwd_context.hash(
                    request.new_password)

                session.add(user)
                session.commit()
                session.refresh(user)

            return auth_pb2.EmptyResponse()

        except ValueError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))
            return auth_pb2.RegistrationResponse()
