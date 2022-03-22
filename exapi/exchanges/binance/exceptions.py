from exapi.exceptions import ExchangeError
from exapi.models import Request, Response


class BinanceError(ExchangeError):
    "Base error for binance rest api."

    def __str__(self) -> str:
        return "Binance exchange error."


class BinanceInvalidSymbolError(BinanceError):
    """Will be raised when symbol does not exist on exchange."""

    def __init__(
        self, request: Request, response: Response
    ) -> None:
        super().__init__(request, response)

    def __str__(self) -> str:
        return "Invalid symbol."
