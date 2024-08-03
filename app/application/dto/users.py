from dataclasses import dataclass
from uuid import UUID
from pydantic import EmailStr

# entities
from app.domain.entities.users import UserEntity


@dataclass
class CreateUserRequest:
    email: EmailStr
    password: str


@dataclass
class LoginUserRequest:
    email: EmailStr
    password: str


@dataclass
class UserResponse:
    id: UUID
    email: EmailStr

    @classmethod
    def from_entity(cls, entity: UserEntity) -> "UserResponse":
        return cls(
            id=entity.id.value,
            email=entity.email
        )
