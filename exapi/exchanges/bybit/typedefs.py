from typing import Literal, TypedDict

BybitOrderStatus = Literal[
    "NEW",
    "PARTIALLY_FILLED",
    "FILLED",
    "CANCELED",
    "PENDING_CANCEL",
    "PENDING_NEW",
    "REJECTED",
]
BybitOrderType = Literal["LIMIT", "MARKET", "LIMIT_MAKER"]
BybitOrderSide = Literal["Buy", "Sell"]
BybitTimeInForce = Literal["GTC", "FOK", "IOC"]


class BybitSymbolInfo(TypedDict):
    name: str
    alias: str
    baseCurrency: str
    quoteCurrency: str
    basePrecision: str
    quotePrecision: str
    minTradeQuantity: str
    minTradeAmount: str
    minPricePrecision: str
    maxTradeQuantity: str
    maxTradeAmount: str
    category: int


class BybitSymbolTicker(TypedDict):
    symbol: str
    bidPrice: str
    bidQty: str
    askPrice: str
    askQty: str
    time: int


class BybitAccountBalance(TypedDict):
    coin: str
    coinId: str
    coinName: str
    total: str
    free: str
    locked: str


class BybitWalletBalance(TypedDict):
    balances: list[BybitAccountBalance]


class BybitOrder(TypedDict):
    accountId: str
    symbol: str
    symbolName: str
    orderLinkId: str
    orderId: str
    transactTime: str
    price: str
    origQty: str
    executedQty: str
    status: BybitOrderStatus
    timeInForce: BybitTimeInForce
    type: BybitOrderType
    side: BybitOrderSide
