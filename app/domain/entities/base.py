from dataclasses import dataclass

from app.domain.value_objects.id import IdVO


@dataclass
class BaseEntity:
    id: IdVO
