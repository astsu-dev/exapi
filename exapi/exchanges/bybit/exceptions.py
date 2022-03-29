from exapi.exceptions import ExchangeError


class BybitError(ExchangeError):
    """Will be raised when response is not successful."""

    def __str__(self) -> str:
        return "Bybit error."


class BybitInvalidSymbolError(BybitError):
    """Will be raised when symbol does not exist."""

    def __str__(self) -> str:
        return "Invalid symbol error."
