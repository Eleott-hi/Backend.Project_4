from typing import Any
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer

import grpc
from proto import auth_pb2, auth_pb2_grpc


async def middleware_get_token_from_cookies(request: Request, call_next):
    token = request.cookies.get("JWToken")

    if "authorization" not in request.headers and token:
        request.scope['headers'].append(
            (b'authorization',  b'Bearer ' + token.encode())
        )

    return await call_next(request)


class JWTBearer(HTTPBearer):

    async def __call__(self, request: Request) -> Any:
        cridentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

        token = await super().__call__(request)

        if token is None:
            raise cridentials_exception

        if not self.verify_jwt(token.credentials):
            raise cridentials_exception

        return token

    def verify_jwt(self, token: str) -> bool:
        try:

            channel = grpc.insecure_channel('auth:50051')
            stub = auth_pb2_grpc.AuthenticationStub(channel)
            stub.VerifyJWT(auth_pb2.VerifyJWTRequest(token=token))

            return True

        except Exception as e:
            print("EXCEPTION:", e, flush=True)

            return False
