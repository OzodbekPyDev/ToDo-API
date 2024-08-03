from uuid import UUID, uuid4

# adapters [domain]
from app.domain.protocols.adapters.id_provider import IdProvider


class SystemIdProvider(IdProvider):
    def generate_uuid(self) -> UUID:
        return uuid4()
