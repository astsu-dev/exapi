from exapi.exceptions import ExchangeError


class BinanceError(ExchangeError):
    "Base error for binance rest api."

    def __str__(self) -> str:
        return "Binance exchange error."


class BinanceInvalidSymbolError(BinanceError):
    """Will be raised when symbol does not exist on exchange."""

    def __str__(self) -> str:
        return "Invalid symbol."


class BinanceAuthError(BinanceError):
    """Will be raised when account api keys are not valid."""

    def __str__(self) -> str:
        return "Invalid api keys."


class BinanceBadPrecisionError(BinanceError):
    """Will be raised when precision is over the maximum defined for this asset."""

    def __str__(self) -> str:
        return "Precision is over the maximum defined for this asset."


class BinanceBadRecvWindowError(BinanceError):
    """Will be raised when recv window is not valid."""

    def __str__(self) -> str:
        return "Recv window must be less than 60000."
