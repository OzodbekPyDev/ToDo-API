from datetime import timedelta
from uuid import UUID
from jose import jwt
from jose import JWTError

# fastapi
from fastapi import Request

# adapters [domain]
from app.domain.protocols.adapters.jwt_processor import JwtTokenProcessor
from app.domain.protocols.adapters.datetime_provider import DateTimeProvider
from app.domain.value_objects.id import IdVO

# config
from app.infrastructure.config import settings


class JoseJwtTokenProcessor(JwtTokenProcessor):

    def __init__(
            self,
            datetime_provider: DateTimeProvider,
            request: Request
    ) -> None:
        self.datetime_provider = datetime_provider
        self.request = request

    def generate_token(self, user_id: IdVO) -> str:
        issued_at = self.datetime_provider.get_current_time()

        expiration_time = issued_at + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        claims = {
            "iat": issued_at,
            "exp": expiration_time,
            "sub": str(user_id.value)
        }

        return jwt.encode(
            claims=claims,
            key=settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )

    def validate_token(self, token: str) -> IdVO | None:

        try:
            payload = jwt.decode(
                token=token,
                key=settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )

            return IdVO(value=UUID(payload["sub"]))

        except (JWTError, KeyError, ValueError):
            return None

    def get_current_user_id(self) -> IdVO | None:
        token = self.request.auth
        user_id = self.validate_token(token)
        return user_id
