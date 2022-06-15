from exapi.exceptions import ExchangeError


class BybitError(ExchangeError):
    """Will be raised when response is not successful."""

    def __str__(self) -> str:
        return f"Bybit error: {self.response}"


class BybitInvalidSymbolError(BybitError):
    """Will be raised when symbol does not exist."""

    def __str__(self) -> str:
        return "Invalid symbol error."


class BybitAuthError(BybitError):
    """Will be raised when api keys are not valid.
    Can be raised if signature is not valid (example: symbol is not valid).
    """

    def __str__(self) -> str:
        return "Invalid api keys."


class BybitInvalidPriceDecimalsError(BybitError):
    """Will be raised when order price decimal too long."""

    def __str__(self) -> str:
        return "Order price decimal too long."


class BybitInvalidQuantityDecimalsError(BybitError):
    """Will be raised when order quantity has too many decimals."""

    def __str__(self) -> str:
        return "Order quantity has too many decimals."


class BybitInsufficientBalanceError(BybitError):
    """Will be raised when insufficient balance for create order."""

    def __str__(self) -> str:
        return "Insufficient balance."


class BybitInvalidParameterError(BybitError):
    """Will be raised when invalid parameter sent."""

    def __str__(self) -> str:
        return "Invalid parameter sent."


class BybitTooHighPriceError(BybitError):
    """Will be raised when order price exceeded upper limit."""

    def __str__(self) -> str:
        return "Order price exceeded upper limit."


class BybitTooLowPriceError(BybitError):
    """Will be raised when order price exceeded lower limit."""

    def __str__(self) -> str:
        return "Order price exceeded lower limit."


class BybitTooHighQuantityError(BybitError):
    """Will be raised when order quantity exceeded upper limit."""

    def __str__(self) -> str:
        return "Order quantity exceeded upper limit."


class BybitTooLowQuantityError(BybitError):
    """Will be raised when order quantity exceeded lower limit."""

    def __str__(self) -> str:
        return "Order quantity exceeded lower limit."
