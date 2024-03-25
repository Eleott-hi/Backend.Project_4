from fastapi import APIRouter, status,  HTTPException, Request, Depends
from auth.JWTBearer import JWTBearer
from fastapi.responses import JSONResponse
from services.Interfaces.IClientService import IClientService
from uuid import UUID

import grpc
from proto import auth_pb2, auth_pb2_grpc
from routers.schemas import RegistrationRequest, LoginRequest, ChangePasswordRequest, ForgotPasswordRequest


class AuthRouter():
    def __init__(self):
        self.router = APIRouter(prefix="/auth", tags=["Authentication"])

        @self.router.post("/register")
        async def register(request: RegistrationRequest) -> JSONResponse:
            """
            Register new

            Parameters:
            - `request`: `RegistrationRequest` object containing client data.

            Returns:
            - `JSONResponse` object containing token.
            """
            try:

                d = request.__dict__
                # d['password'] = ""
                stub = self.__get_stub()
                response: auth_pb2.RegistrationResponse = stub.Registration(
                    auth_pb2.RegistrationRequest(**d)
                )

                res = JSONResponse(
                    status_code=status.HTTP_201_CREATED,
                    content={"token": response.token},
                )

                res.set_cookie(
                    key="JWToken",
                    value=response.token,
                    httponly=True,
                )

                return res

            except grpc.RpcError as e:
                self.__handle_grpc_exceptions(e)

            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=e,
                )

        @self.router.post("/login")
        async def login(request: LoginRequest) -> dict:
            """
            Login

            Parameters:
            - `request`: `LoginRequest` object containing client data.

            Returns:
            - `JSONResponse` object containing token.
            """
            try:
                stub = self.__get_stub()
                response: auth_pb2.RegistrationResponse = stub.Login(
                    auth_pb2.LoginRequest(**request.__dict__)
                )

                res = JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={"token": response.token},
                )

                res.set_cookie(
                    key="JWToken",
                    value=response.token,
                    httponly=True
                )

                return res

            except grpc.RpcError as e:
                self.__handle_grpc_exceptions(e)

            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=e,
                )

        @self.router.post("/forgot-password")
        async def forgot_password(request: ForgotPasswordRequest) -> dict:
            """
            Forgot password

            Parameters:
            - `request`: `ForgotPasswordRequest` object containing client data.

            Returns:
            - `JSONResponse` object containing token.
            """
            try:
                stub = self.__get_stub()
                response: auth_pb2.RegistrationResponse = stub.ForgotPassword(
                    auth_pb2.ForgotPasswordRequest(**request.__dict__)
                )

                return {"token": response.token}

            except grpc.RpcError as e:
                self.__handle_grpc_exceptions(e)

            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=e,
                )

        @self.router.post("/change-password", dependencies=[Depends(JWTBearer())])
        async def change_password(request: ChangePasswordRequest) -> dict:
            """
            Change password

            Parameters:
            - `request`: `ChangePasswordRequest` object containing client data.

            Returns:
            - `JSONResponse` object containing token.
            """
            try:
                stub = self.__get_stub()
                stub.ChangePassword(
                    auth_pb2.ChangePasswordRequest(**request.__dict__)
                )

                return {"message": "Password changed"}

            except grpc.RpcError as e:
                self.__handle_grpc_exceptions(e)

            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=e,
                )

    def __get_stub(self):
        channel = grpc.insecure_channel('auth:50051')
        stub = auth_pb2_grpc.AuthenticationStub(channel)
        return stub

    def __handle_grpc_exceptions(self, e: grpc.RpcError):

        match e.code():
            case grpc.StatusCode.INVALID_ARGUMENT:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=e.details(),
                )
            case grpc.StatusCode.UNAUTHENTICATED:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=e.details(),
                )
            case grpc.StatusCode.PERMISSION_DENIED:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=e.details(),
                )
            case grpc.StatusCode.NOT_FOUND:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=e.details(),
                )
            case  grpc.StatusCode.ALREADY_EXISTS:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=e.details(),
                )
            case _:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=e.details(),
                )
