from uuid import UUID

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, unique=True)
