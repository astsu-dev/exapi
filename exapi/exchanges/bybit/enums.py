class BybitOrderSideEnum:
    BUY = "Buy"
    SELL = "Sell"


class BybitOrderTypeEnum:
    LIMIT = "LIMIT"
    MARKET = "MARKET"
    LIMIT_MAKER = "LIMIT_MAKER"


class BybitOrderStatusEnum:
    NEW = "NEW"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELED = "CANCELED"
    PENDING_CANCELED = "PENDING_CANCELED"
    PENDING_NEW = "PENDING_NEW"
    REJECTED = "REJECTED"


class BybitTimeInForceEnum:
    GTC = "GTC"
    FOK = "FOK"
    IOC = "IOC"
