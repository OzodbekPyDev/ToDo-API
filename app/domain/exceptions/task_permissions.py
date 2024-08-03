from app.domain.exceptions.base import DomainException


class PermissionDeniedException(DomainException):
    """Permission denied exception"""

    pass


class TaskPermissionNotFoundException(DomainException):
    """Task permission not found exception"""

    pass
