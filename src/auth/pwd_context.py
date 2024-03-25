
from passlib.context import CryptContext
from passlib.pwd import genword


class PWDContext():
    def __init__(self) -> None:
        super().__init__()
        self.crypt_context = CryptContext(
            schemes=["bcrypt"], deprecated="auto")

    def hash(self, password):
        return self.crypt_context.hash(password)

    def verify(self, password, hash):
        return self.crypt_context.verify(password, hash)

    def gen_password(self):
        return genword()
