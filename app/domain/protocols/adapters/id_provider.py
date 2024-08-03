from typing import Protocol
from uuid import UUID


class IdProvider(Protocol):
    def generate_uuid(self) -> UUID:
        raise NotImplementedError
