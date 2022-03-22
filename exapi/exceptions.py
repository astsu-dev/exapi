from exapi.models import Request, Response


class RESTError(Exception):
    """All exceptions will be derived from this exception."""

    def __init__(self, request: Request) -> None:
        self.request = request


class ExchangeError(RESTError):
    """Will be raised when the response from exchange is error.

    Can will be raised if the error from exchange is unknown.
    """

    def __init__(self, request: Request, response: Response) -> None:
        super().__init__(request)
        self.response = response

    def __str__(self) -> str:
        return f"Exchange error."


class RESTNetworkError(RESTError):
    """Will be raised when there are problems with network."""


class RESTNotConnectionError(RESTNetworkError):
    """Will be raised when can not connect to server."""

    def __str__(self) -> str:
        return "Cannot connect to a server."


class RESTConnectionTimeoutError(RESTNetworkError):
    """Will be raised when exceed connection timeout."""

    def __str__(self) -> str:
        return "Connection timeout exceeded."
