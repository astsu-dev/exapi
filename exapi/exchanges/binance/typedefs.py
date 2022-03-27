from typing import Literal, TypedDict

BinanceOrderSide = Literal["BUY", "SELL"]
BinanceOrderType = Literal[
    "LIMIT",
    "MARKET",
    "STOP_LOSS",
    "STOP_LOSS_LIMIT",
    "TAKE_PROFIT",
    "TAKE_PROFIT_LIMIT",
    "LIMIT_MAKER",
]
BinanceOrderStatus = Literal[
    "NEW",
    "PARTIALLY_FILLED",
    "FILLED",
    "CANCELED",
    "PENDING_CANCEL",
    "REJECTED",
    "EXPIRED",
]
BinanceOrderResponseType = Literal["ACK", "RESULT", "FULL"]
BinanceTimeInForce = Literal["GTC", "IOC", "FOK"]
BinancePermission = Literal["SPOT", "MARGIN", "LEVERAGED", "TRD_GRP_002"]
BinanceAccountType = Literal["SPOT"]  # TODO: extend possible values


class BinanceRateLimit(TypedDict):
    rateLimitType: Literal["REQUEST_WEIGHT", "ORDERS", "RAW_REQUEST"]
    interval: Literal["SECOND", "MINUTE", "DAY"]
    intervalNum: int
    limit: int


class BinanceExchangeMaxNumOrdersFilter(TypedDict):
    filterType: Literal["EXCHANGE_MAX_NUM_ORDERS"]
    maxNumOrders: int


class BinanceExchangeMaxNumAlgoOrdersFilter(TypedDict):
    filterType: Literal["EXCHANGE_MAX_NUM_ALGO_ORDERS"]
    maxNumAlgoOrders: int


BinanceExchangeFilter = (
    BinanceExchangeMaxNumOrdersFilter | BinanceExchangeMaxNumAlgoOrdersFilter
)


class BinanceSymbolPriceFilter(TypedDict):
    filterType: Literal["PRICE_FILTER"]
    minPrice: str
    maxPrice: str
    tickSize: str


class BinanceSymbolPercentPriceFilter(TypedDict):
    filterType: Literal["PERCENT_PRICE"]
    multiplierUp: str
    multiplierDown: str
    avgPriceMins: int


class BinanceSymbolPercentPriceBySideFilter(TypedDict):
    filterType: Literal["PERCENT_PRICE_BY_SIDE"]
    bidMultiplierUp: str
    bidMultiplierDown: str
    askMultiplierUp: str
    askMultiplierDown: str
    avgPriceMins: int


class BinanceSymbolLotSizeFilter(TypedDict):
    filterType: Literal["LOT_SIZE"]
    minQty: str
    maxQty: str
    stepSize: str


class BinanceSymbolMinNotionalFilter(TypedDict):
    filterType: Literal["MIN_NOTIONAL"]
    minNotional: str
    applyToMarket: bool
    avgPriceMins: int


class BinanceSymbolIcebergPartsFilter(TypedDict):
    filterType: Literal["ICEBERG_PARTS"]
    limit: int


class BinanceSymbolMarketLotSizeFilter(TypedDict):
    filterType: Literal["MARKET_LOT_SIZE"]
    minQty: str
    maxQty: str
    stepSize: str


class BinanceSymbolMaxNumOrdersFilter(TypedDict):
    filterType: Literal["MAX_NUM_ORDERS"]
    maxNumOrders: int


class BinanceSymbolMaxNumAlgoOrdersFilter(TypedDict):
    filterType: Literal["MAX_NUM_ALGO_ORDERS"]
    maxNumAlgoOrders: int


class BinanceSymbolMaxNumIcebergOrdersFilter(TypedDict):
    filterType: Literal["MAX_NUM_ICEBERG_ORDERS"]
    maxNumIcebergOrders: int


class BinanceSymbolMaxPositionFilter(TypedDict):
    filterType: Literal["MAX_POSITION"]
    maxPosition: str


BinanceSymbolFilter = (
    BinanceSymbolPriceFilter
    | BinanceSymbolPercentPriceFilter
    | BinanceSymbolPercentPriceBySideFilter
    | BinanceSymbolLotSizeFilter
    | BinanceSymbolMinNotionalFilter
    | BinanceSymbolIcebergPartsFilter
    | BinanceSymbolMarketLotSizeFilter
    | BinanceSymbolMaxNumOrdersFilter
    | BinanceSymbolMaxNumAlgoOrdersFilter
    | BinanceSymbolMaxNumIcebergOrdersFilter
    | BinanceSymbolMaxPositionFilter
)


class BinanceSymbolInfo(TypedDict):
    symbol: str
    status: Literal[
        "PRE_TRADING",
        "TRADING",
        "POST_TRADING",
        "END_OF_DAY",
        "HALT",
        "AUCTION_MATCH",
        "BREAK",
    ]
    baseAsset: str
    baseAssetPrecision: int
    quoteAsset: str
    quotePrecision: int
    quoteAssetPrecision: int
    orderTypes: list[BinanceOrderType]
    icebergAllowed: bool
    ocoAllowed: bool
    quoteOrderQtyMarketAllowed: bool
    isSpotTradingAllowed: bool
    isMarginTradingAllowed: bool
    filters: list[BinanceSymbolFilter]
    permissions: list[BinancePermission]


class BinanceExchangeInfo(TypedDict):
    timezone: str
    serverTime: int
    rateLimits: list[BinanceRateLimit]
    exchangeFilters: list[BinanceExchangeFilter]
    symbols: list[BinanceSymbolInfo]


class BinanceSymbolTicker(TypedDict):
    """Symbol order book ticker type."""

    symbol: str
    bidPrice: str
    bidQty: str
    askPrice: str
    askQty: str


class BinanceAckOrderResponse(TypedDict):
    symbol: str
    orderId: int
    orderListId: int
    clientOrderId: str
    transactTime: int


class BinanceResultOrderResponse(BinanceAckOrderResponse):
    price: str
    origQty: str
    executedQty: str
    cummulativeQuoteQty: str
    status: BinanceOrderStatus
    timeInForce: BinanceTimeInForce
    type: BinanceOrderType
    side: BinanceOrderSide


class BinanceFilledOrder(TypedDict):
    price: str
    qty: str
    commission: str
    commissionAsset: str
    tradeId: int


class BinanceFullOrderResponse(BinanceResultOrderResponse):
    fills: list[BinanceFilledOrder]


class BinanceAccountBalance(TypedDict):
    asset: str
    free: str
    locked: str


class BinanceAccountInfo(TypedDict):
    makerCommission: int
    takerCommission: int
    buyerCommission: int
    sellerCommission: int
    canTrade: bool
    canWithdraw: bool
    canDeposit: bool
    updateTime: int
    accountType: BinanceAccountType
    balances: list[BinanceAccountBalance]
    permissions: list[BinancePermission]
