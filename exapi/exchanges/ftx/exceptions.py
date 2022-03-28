from exapi.exceptions import ExchangeError


class FTXError(ExchangeError):
    def __str__(self) -> str:
        return "FTX error."


class FTXInvalidMarketError(FTXError):
    """Will be raised if market does not exist on exchange."""

    def __str__(self) -> str:
        return "Invalid market error."
