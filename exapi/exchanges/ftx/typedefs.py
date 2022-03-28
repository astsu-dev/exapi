from typing import Literal, TypedDict

FTXMarketType = Literal["spot", "future"]


class FTXMarket(TypedDict):
    name: str
    baseCurrency: str | None
    quoteCurrency: str | None
    quoteVolume24h: float
    change1h: float
    change24h: float
    changeBod: float
    highLeverageFeeExempt: bool
    minProvideSize: float
    type: FTXMarketType
    underlying: str
    enabled: bool
    ask: float
    bid: float
    last: float
    postOnly: bool
    price: float
    priceIncrement: float
    sizeIncrement: float
    restricted: bool
    volumeUsd24h: float
    largeOrderThreshold: float


class FTXOrderbook(TypedDict):
    asks: list[tuple[float, float]]
    bids: list[tuple[float, float]]
