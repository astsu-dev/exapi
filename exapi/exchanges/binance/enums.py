class BinanceOrderSideEnum:
    BUY = "BUY"
    SELL = "SELL"


class BinanceOrderTypeEnum:
    LIMIT = "LIMIT"
    MARKET = "MARKET"
    STOP_LOSS = "STOP_LOSS"
    STOP_LOSS_LIMIT = "STOP_LOSS_LIMIT"
    TAKE_PROFIT = "TAKE_PROFIT"
    TAKE_PROFIT_LIMIT = "TAKE_PROFIT_LIMIT"
    LIMIT_MAKER = "LIMIT_MAKER"


class BinanceTimeInForceEnum:
    GTC = "GTC"
    IOC = "IOC"
    FOK = "FOK"


class BinanceOrderResponseTypeEnum:
    ACK = "ACK"
    RESULT = "RESULT"
    FULL = "FULL"
