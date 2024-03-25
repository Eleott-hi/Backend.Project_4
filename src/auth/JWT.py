
import jwt
from datetime import datetime, timedelta
from config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_ACCESS_TOKEN_EXPIRE_MINUTES


class JWT():

    def get_token(self):
        print(JWT_SECRET_KEY, flush=True)

        return jwt.encode(
            {
                "role": "user",
                "exp": self.__exp(),
            },
            JWT_SECRET_KEY,
            algorithm=JWT_ALGORITHM,
        )

    def verify_token(self, token):
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])

    def __exp(self):
        return int((datetime.now() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp())
