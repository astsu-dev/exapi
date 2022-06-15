from exapi.exceptions import ExchangeError


class BybitError(ExchangeError):
    """Will be raised when response is not successful."""

    def __str__(self) -> str:
        return f"Bybit error: {self.msg}"


class BybitInvalidSymbolError(BybitError):
    """Will be raised when symbol does not exist."""

    def __str__(self) -> str:
        return f"Invalid symbol error. {self.msg}"


class BybitAuthError(BybitError):
    """Will be raised when api keys are not valid.
    Can be raised if signature is not valid (example: symbol is not valid).
    """

    def __str__(self) -> str:
        return f"Invalid api keys. {self.msg}"


class BybitInvalidPriceDecimalsError(BybitError):
    """Will be raised when order price decimal too long."""

    def __str__(self) -> str:
        return f"Order price decimal too long. {self.msg}"


class BybitInvalidQuantityDecimalsError(BybitError):
    """Will be raised when order quantity has too many decimals."""

    def __str__(self) -> str:
        return f"Order quantity has too many decimals. {self.msg}"


class BybitInsufficientBalanceError(BybitError):
    """Will be raised when insufficient balance for create order."""

    def __str__(self) -> str:
        return f"Insufficient balance. {self.msg}"


class BybitInvalidParameterError(BybitError):
    """Will be raised when invalid parameter sent."""

    def __str__(self) -> str:
        return f"Invalid parameter sent. {self.msg}"


class BybitTooHighPriceError(BybitError):
    """Will be raised when order price exceeded upper limit."""

    def __str__(self) -> str:
        return f"Order price exceeded upper limit. {self.msg}"


class BybitTooLowPriceError(BybitError):
    """Will be raised when order price exceeded lower limit."""

    def __str__(self) -> str:
        return f"Order price exceeded lower limit. {self.msg}"


class BybitTooHighQuantityError(BybitError):
    """Will be raised when order quantity exceeded upper limit."""

    def __str__(self) -> str:
        return f"Order quantity exceeded upper limit. {self.msg}"


class BybitTooLowQuantityError(BybitError):
    """Will be raised when order quantity exceeded lower limit."""

    def __str__(self) -> str:
        return f"Order quantity exceeded lower limit. {self.msg}"
