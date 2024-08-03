from app.domain.exceptions.base import DomainException


class UserAlreadyExistsException(DomainException):
    """User already exists exception"""

    pass


class UserNotFoundException(DomainException):
    """User not found exception"""

    pass


class InvalidAuthCredentialsException(DomainException):
    """Invalid authorization credentials exception"""

    pass
