from app.domain.exceptions.base import DomainException


class TaskNotFoundException(DomainException):
    """Task not found exception"""

    pass
