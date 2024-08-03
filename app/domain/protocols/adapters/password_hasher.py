from typing import Protocol


class PasswordHasher(Protocol):

    def hash_password(self, password: str) -> str:
        raise NotImplementedError

    def verify_password(self, password: str, hashed_password: str) -> bool:
        raise NotImplementedError
