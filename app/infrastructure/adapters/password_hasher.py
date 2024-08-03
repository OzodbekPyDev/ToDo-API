from app.domain.protocols.adapters.password_hasher import PasswordHasher
from passlib.handlers.pbkdf2 import pbkdf2_sha256


class Pbkdf2PasswordHasher(PasswordHasher):

    def hash_password(self, password: str) -> str:
        return pbkdf2_sha256.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return pbkdf2_sha256.verify(password, hashed_password)
