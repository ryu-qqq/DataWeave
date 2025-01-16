class ForbiddenException(Exception):
    """Exception raised when the API token has expired."""


class UnauthorizedException(Exception):
    """Exception raised when the API token has expired."""


class TooManyRequestException(Exception):
    """Exception raised when the Too Many Request has been sent."""


class UnExpectedException(Exception):
    """Exception raised when Unexpected Response has been received."""
