"""
Common exceptions for the core application.
"""

from django.core.exceptions import ValidationError as DjangoValidationError
from ninja.errors import HttpError


class ApplicationError(Exception):
    """Base application error."""

    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        super().__init__(message)


class NotFoundError(ApplicationError):
    """Resource not found error."""

    pass


class ValidationError(ApplicationError):
    """Validation error."""

    def __init__(self, message: str, field: str = None, error_code: str = None):
        self.field = field
        super().__init__(message, error_code)


class PermissionError(ApplicationError):
    """Permission denied error."""

    pass


class BusinessLogicError(ApplicationError):
    """Business logic error."""

    pass


class SoftDeletedError(ApplicationError):
    """Accessing soft-deleted object error."""

    pass


class ConcentrationLevelError(ValidationError):
    """Concentration level validation error."""

    pass


class StudyEnvironmentError(ValidationError):
    """Study environment validation error."""

    pass


class AchievementError(ApplicationError):
    """Achievement related error."""

    pass


def handle_django_validation_error(error: DjangoValidationError) -> ValidationError:
    """Convert Django validation error to application validation error."""
    if hasattr(error, "message_dict"):
        # Multiple field errors
        messages = []
        for field, field_errors in error.message_dict.items():
            messages.append(f"{field}: {', '.join(field_errors)}")
        return ValidationError("; ".join(messages))
    else:
        # Single error
        return ValidationError(str(error))


def handle_http_error(status_code: int, message: str) -> HttpError:
    """Create HTTP error for API responses."""
    return HttpError(status_code, message)
