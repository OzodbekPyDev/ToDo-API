from dishka import Provider, Scope, provide, from_context
from dishka.integrations.fastapi import FromDishka
from fastapi import Request

# adapters [domain]
from app.domain.protocols.adapters.id_provider import IdProvider
from app.domain.protocols.adapters.datetime_provider import DateTimeProvider
from app.domain.protocols.adapters.password_hasher import PasswordHasher
from app.domain.protocols.adapters.jwt_processor import JwtTokenProcessor

# adapters [infrastructure]
from app.infrastructure.adapters.id_provider import SystemIdProvider
from app.infrastructure.adapters.datetime_provider import SystemDateTimeProvider, Timezone
from app.infrastructure.adapters.password_hasher import Pbkdf2PasswordHasher
from app.infrastructure.adapters.jwt_processor import JoseJwtTokenProcessor


class AdaptersProvider(Provider):
    request = from_context(
        scope=Scope.REQUEST,
        provides=Request,
    )

    @provide(scope=Scope.REQUEST)
    def provide_jwt_processor(
            self,
            datetime_provider: FromDishka[DateTimeProvider],
            request: Request,
    ) -> JwtTokenProcessor:
        return JoseJwtTokenProcessor(
            datetime_provider=datetime_provider,
            request=request
        )

    @provide(scope=Scope.APP)
    def provide_id_provider(self) -> IdProvider:
        return SystemIdProvider()

    @provide(scope=Scope.APP)
    def provide_datetime_provider(self) -> DateTimeProvider:
        return SystemDateTimeProvider(tz=Timezone.UTC)

    @provide(scope=Scope.APP)
    def provide_password_hasher(self) -> PasswordHasher:
        return Pbkdf2PasswordHasher()
