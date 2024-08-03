from typing import Protocol

# value objects
from app.domain.value_objects.id import IdVO


class JwtTokenProcessor(Protocol):

    def generate_token(self, user_id: IdVO) -> str:
        raise NotImplementedError

    def validate_token(self, token: str) -> IdVO | None:
        raise NotImplementedError

    def get_current_user_id(self) -> IdVO | None:
        raise NotImplementedError
