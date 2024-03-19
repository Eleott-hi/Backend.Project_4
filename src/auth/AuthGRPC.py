import auth_pb2
import auth_pb2_grpc

# from servicies.Interfacies.IAuthService import IAuthenticationService
from database.Models.User import User
from database.database import engine, Session


class AuthenticationServicer(auth_pb2_grpc.AuthenticationServicer):
    def Login(self, request: auth_pb2.LoginRequest, context):
        return auth_pb2.LoginResponse(token="user.password_token")

    def Registration(self, request: auth_pb2.RegistrationRequest, context):
        print("HERE", request.__dict__, flush=True)

        with Session(engine) as session:
            user = User(
                name=request.name,
                surname=request.surname,
                email=request.email,
                phone_number=request.phone_number,
                password_token=request.password,
            )
            session.add(user)
            session.commit()
            session.refresh(user)

        return auth_pb2.RegistrationResponse(token="token")

    def ForgotPassword(self, request: auth_pb2.ForgotPasswordRequest, context):
        return auth_pb2.EmptyResponse()

    def ChangePassword(self, request: auth_pb2.ChangePasswordRequest, context):
        return auth_pb2.EmptyResponse()

    