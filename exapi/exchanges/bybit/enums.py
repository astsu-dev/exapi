class BybitOrderSide:
    BUY = "Buy"
    SELL = "Sell"


class BybitOrderType:
    LIMIT = "LIMIT"
    MARKET = "MARKET"
    LIMIT_MAKER = "LIMIT_MAKER"


class BybitOrderStatus:
    NEW = "NEW"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELED = "CANCELED"
    PENDING_CANCELED = "PENDING_CANCELED"
    PENDING_NEW = "PENDING_NEW"
    REJECTED = "REJECTED"


class BybitTimeInForce:
    GTC = "GTC"
    FOK = "FOK"
    IOC = "IOC"
