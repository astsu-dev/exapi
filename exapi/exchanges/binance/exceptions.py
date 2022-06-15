from exapi.exceptions import ExchangeError


class BinanceError(ExchangeError):
    "Base error for binance rest api."

    def __str__(self) -> str:
        return f"Binance error: {self.msg}"


class BinanceInvalidSymbolError(BinanceError):
    """Will be raised when symbol does not exist on exchange."""

    def __str__(self) -> str:
        return f"Invalid symbol. {self.msg}"


class BinanceAuthError(BinanceError):
    """Will be raised when account api keys are not valid."""

    def __str__(self) -> str:
        return f"Invalid api keys. {self.msg}"


class BinanceBadPrecisionError(BinanceError):
    """Will be raised when precision is over the maximum defined for this asset."""

    def __str__(self) -> str:
        return f"Precision is over the maximum defined for this asset. {self.msg}"


class BinanceBadRecvWindowError(BinanceError):
    """Will be raised when recv window is not valid."""

    def __str__(self) -> str:
        return f"Recv window must be less than 60000. {self.msg}"
