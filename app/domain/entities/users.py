from dataclasses import dataclass

from app.domain.entities.base import BaseEntity

from app.domain.value_objects.id import IdVO


@dataclass
class UserEntity(BaseEntity):
    email: str
    password: str

    def __init__(
            self,
            id: IdVO,
            email: str,
            password: str
    ) -> None:
        self.id = id
        self.email = email
        self.password = password

    def update(
            self,
            email: str,
            password: str
    ) -> None:
        self.email = email
        self.password = password
