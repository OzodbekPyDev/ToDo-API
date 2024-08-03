from fastapi import FastAPI

# exceptions[domain]
# users
from app.domain.exceptions.users import (
    UserAlreadyExistsException,
    UserNotFoundException,
    InvalidAuthCredentialsException
)
# tasks
from app.domain.exceptions.tasks import (
    TaskNotFoundException
)
# task permissions
from app.domain.exceptions.task_permissions import (
    PermissionDeniedException,
    TaskPermissionNotFoundException
)

# exception handlers
# users
from app.infrastructure.exception_handlers.users import (
    user_already_exists_exception_handler,
    user_not_found_exception_handler,
    invalid_auth_credentials_exception_handler
)
# tasks
from app.infrastructure.exception_handlers.tasks import (
    task_not_found_exception_handler
)
# task permissions
from app.infrastructure.exception_handlers.task_permissions import (
    permission_denied_exception_handler,
    task_permission_not_found_exception_handler
)


def init_exception_handlers(app: FastAPI) -> None:
    # users
    app.add_exception_handler(
        exc_class_or_status_code=UserAlreadyExistsException,
        handler=user_already_exists_exception_handler
    )
    app.add_exception_handler(
        exc_class_or_status_code=UserNotFoundException,
        handler=user_not_found_exception_handler
    )
    app.add_exception_handler(
        exc_class_or_status_code=InvalidAuthCredentialsException,
        handler=invalid_auth_credentials_exception_handler
    )

    # tasks
    app.add_exception_handler(
        exc_class_or_status_code=TaskNotFoundException,
        handler=task_not_found_exception_handler
    )

    # task permissions
    app.add_exception_handler(
        exc_class_or_status_code=PermissionDeniedException,
        handler=permission_denied_exception_handler
    )
    app.add_exception_handler(
        exc_class_or_status_code=TaskPermissionNotFoundException,
        handler=task_permission_not_found_exception_handler
    )
