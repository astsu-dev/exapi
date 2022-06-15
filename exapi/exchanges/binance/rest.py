from types import TracebackType
from typing import Any, DefaultDict, Iterable, Literal, Type, cast, overload

import aiohttp

from exapi.base.rest import BaseExchangeREST
from exapi.exchanges.binance.enums import BinanceOrderTypeEnum
from exapi.exchanges.binance.exceptions import (
    BinanceAuthError,
    BinanceBadPrecisionError,
    BinanceBadRecvWindowError,
    BinanceError,
    BinanceInvalidSymbolError,
)
from exapi.exchanges.binance.models import BinanceCredentials
from exapi.exchanges.binance.typedefs import (
    BinanceAccountInfo,
    BinanceAckOrderResponse,
    BinanceExchangeInfo,
    BinanceFullOrderResponse,
    BinanceOrderResponseType,
    BinanceOrderSide,
    BinanceOrderType,
    BinanceResultOrderResponse,
    BinanceSymbolTicker,
    BinanceTimeInForce,
)
from exapi.exchanges.binance.utils import sign_request
from exapi.models import Request, Response
from exapi.typedefs import HeadersType


class BinanceRESTWithoutCredentials(BaseExchangeREST):
    """Doesn't incapsulate account credentials.
    For private methods you need to provide credentials in params.
    It can be useful if you need to manage multiple accounts.
    You don't need to create multiple instances for each account.
    """

    def __init__(
        self,
        *,
        base_url: str = "https://api.binance.com",
        request_timeout: float | None = None,
    ) -> None:
        super().__init__(base_url=base_url, request_timeout=request_timeout)

    @overload
    async def get_ticker(self, symbol: str) -> BinanceSymbolTicker:
        ...

    @overload
    async def get_ticker(self, symbol: None = None) -> list[BinanceSymbolTicker]:
        ...

    async def get_ticker(
        self, symbol: str | None = None
    ) -> BinanceSymbolTicker | list[BinanceSymbolTicker]:
        """Returns `symbol` order book ticker - best ask and bid orders.

        ```pycon
        >>> import asyncio
        >>> from exapi.exchanges.binance.rest import BinanceRESTWithoutCredentials
        >>> from exapi.exchanges.binance.typedefs import BinanceSymbolTicker
        >>>
        >>> async def get_single_ticker(symbol: str) -> BinanceSymbolTicker:
        ...     async with BinanceRESTWithoutCredentials() as rest:
        ...         return await rest.get_ticker(symbol)
        ...
        >>> asyncio.run(get_single_ticker("LTCBTC"))
        {
            "symbol": "LTCBTC",
            "bidPrice": "4.00000000",
            "bidQty": "431.00000000",
            "askPrice": "4.00000200",
            "askQty": "9.00000000"
        }
        >>>
        >>> async def get_all_tickers() -> list[BinanceSymbolTicker]:
        ...     async with BinanceRESTWithoutCredentials() as rest:
        ...         return await rest.get_ticker()
        ...
        >>> asyncio.run(get_all_tickers())
        [
            {
                "symbol": "LTCBTC",
                "bidPrice": "4.00000000",
                "bidQty": "431.00000000",
                "askPrice": "4.00000200",
                "askQty": "9.00000000"
            },
            {
                "symbol": "ETHBTC",
                "bidPrice": "0.07946700",
                "bidQty": "9.00000000",
                "askPrice": "100000.00000000",
                "askQty": "1000.00000000"
            }
        ]
        ```

        Args:
            symbol: format is "BTCUSDT". If None will be returned tickers for all symbols.

        Returns:
            Symbol ticker or all symbol tickers.

        Raises:
            BinanceInvalidSymbolError: will be raised if `symbol` does not exist.
        """

        params = {}
        if symbol is not None:
            params["symbol"] = symbol

        request = Request(
            method="GET",
            base_url=self._base_url,
            path="/api/v3/ticker/bookTicker",
            params=params,
        )
        response = await self._send_request(request)

        result: BinanceSymbolTicker | list[BinanceSymbolTicker] = response
        return result

    @overload
    async def get_exchange_info(
        self, *, symbol: str, symbols: None = None
    ) -> BinanceExchangeInfo:
        ...

    @overload
    async def get_exchange_info(
        self, *, symbol: None = None, symbols: Iterable[str]
    ) -> BinanceExchangeInfo:
        ...

    @overload
    async def get_exchange_info(
        self, *, symbol: None = None, symbols: None = None
    ) -> BinanceExchangeInfo:
        ...

    async def get_exchange_info(
        self, *, symbol: str | None = None, symbols: Iterable[str] | None = None
    ) -> BinanceExchangeInfo:
        """Returns exchange info.

        ```pycon
        >>> import asyncio
        >>> from exapi.exchanges.binance.rest import BinanceRESTWithoutCredentials
        >>> from exapi.exchanges.binance.typedefs import BinanceExchangeInfo
        >>>
        >>> async def get_exchange_info() -> BinanceExchangeInfo:
        ...     async with BinanceRESTWithoutCredentials() as rest:
        ...         return await rest.get_exchange_info()
        ...
        >>> async def get_exchange_info_with_symbol(symbol: str) -> BinanceExchangeInfo:
        ...     async with BinanceRESTWithoutCredentials() as rest:
        ...         return await rest.get_exchange_info(symbol=symbol)
        ...
        >>> async def get_exchange_info_with_symbols(symbols: list[str]) -> BinanceExchangeInfo:
        ...     async with BinanceRESTWithoutCredentials() as rest:
        ...         return await rest.get_exchange_info(symbols=symbols)
        ...
        >>> asyncio.run(get_exchange_info())
        {
            "timezone": "UTC",
            "serverTime": 1647967664330,
            "rateLimits": [
                {
                    "rateLimitType": "REQUEST_WEIGHT",
                    "interval": "MINUTE",
                    "intervalNum": 1,
                    "limit": 1200
                },
                {
                    "rateLimitType": "ORDERS",
                    "interval": "SECOND",
                    "intervalNum": 10,
                    "limit": 50
                },
                {
                    "rateLimitType": "ORDERS",
                    "interval": "DAY",
                    "intervalNum": 1,
                    "limit": 160000
                },
                {
                    "rateLimitType": "RAW_REQUESTS",
                    "interval": "MINUTE",
                    "intervalNum": 5,
                    "limit": 6100
                }
            ],
            "exchangeFilters": [],
            "symbols": [
                {
                    "symbol": "BNBBTC",
                    "status": "TRADING",
                    "baseAsset": "BNB",
                    "baseAssetPrecision": 8,
                    "quoteAsset": "BTC",
                    "quotePrecision": 8,
                    "quoteAssetPrecision": 8,
                    "baseCommissionPrecision": 8,
                    "quoteCommissionPrecision": 8,
                    "orderTypes": [
                        "LIMIT",
                        "LIMIT_MAKER",
                        "MARKET",
                        "STOP_LOSS_LIMIT",
                        "TAKE_PROFIT_LIMIT"
                    ],
                    "icebergAllowed": True,
                    "ocoAllowed": True,
                    "quoteOrderQtyMarketAllowed": True,
                    "allowTrailingStop": False,
                    "isSpotTradingAllowed": True,
                    "isMarginTradingAllowed": True,
                    "filters": [
                        {
                            "filterType": "PRICE_FILTER",
                            "minPrice": "0.00000100",
                            "maxPrice": "100000.00000000",
                            "tickSize": "0.00000100"
                        },
                        {
                            "filterType": "PERCENT_PRICE",
                            "multiplierUp": "5",
                            "multiplierDown": "0.2",
                            "avgPriceMins": 5
                        },
                        {
                            "filterType": "LOT_SIZE",
                            "minQty": "0.00100000",
                            "maxQty": "100000.00000000",
                            "stepSize": "0.00100000"
                        },
                        {
                            "filterType": "MIN_NOTIONAL",
                            "minNotional": "0.00010000",
                            "applyToMarket": True,
                            "avgPriceMins": 5
                        },
                        {
                            "filterType": "ICEBERG_PARTS",
                            "limit": 10
                        },
                        {
                            "filterType": "MARKET_LOT_SIZE",
                            "minQty": "0.00000000",
                            "maxQty": "21800.92779166",
                            "stepSize": "0.00000000"
                        },
                        {
                            "filterType": "MAX_NUM_ORDERS",
                            "maxNumOrders": 200
                        },
                        {
                            "filterType": "MAX_NUM_ALGO_ORDERS",
                            "maxNumAlgoOrders": 5
                        }
                    ],
                    "permissions": [
                        "SPOT",
                        "MARGIN"
                    ]
                }
            ]
        }
        >>> asyncio.run(get_exchange_info_with_symbol("LTCBTC"))
        {
            "timezone": "UTC",
            "serverTime": 1647967664330,
            "rateLimits": [
                {
                    "rateLimitType": "REQUEST_WEIGHT",
                    "interval": "MINUTE",
                    "intervalNum": 1,
                    "limit": 1200
                },
                ...
            ],
            "exchangeFilters": [],
            "symbols": [
                {
                    "symbol": "LTCBTC",
                    "status": "TRADING",
                    "baseAsset": "LTC",
                    "baseAssetPrecision": 8,
                    "quoteAsset": "BTC",
                    "quotePrecision": 8,
                    "quoteAssetPrecision": 8,
                    "baseCommissionPrecision": 8,
                    "quoteCommissionPrecision": 8,
                    "orderTypes": [
                        "LIMIT",
                        "LIMIT_MAKER",
                        "MARKET",
                        "STOP_LOSS_LIMIT",
                        "TAKE_PROFIT_LIMIT"
                    ],
                    "icebergAllowed": True,
                    "ocoAllowed": True,
                    "quoteOrderQtyMarketAllowed": True,
                    "allowTrailingStop": False,
                    "isSpotTradingAllowed": True,
                    "isMarginTradingAllowed": True,
                    "filters": [
                        {
                            "filterType": "PRICE_FILTER",
                            "minPrice": "0.00000100",
                            "maxPrice": "100000.00000000",
                            "tickSize": "0.00000100"
                        },
                        ...
                    ],
                    "permissions": [
                        "SPOT",
                        "MARGIN"
                    ]
                }
            ]
        }
        >>> asyncio.run(get_exchange_info_with_symbols(["LTCBTC", "BNBBTC"]))
        {
            "timezone": "UTC",
            "serverTime": 1647967664330,
            "rateLimits": [
                {
                    "rateLimitType": "REQUEST_WEIGHT",
                    "interval": "MINUTE",
                    "intervalNum": 1,
                    "limit": 1200
                },
                ...
            ],
            "exchangeFilters": [],
            "symbols": [
                {
                    "symbol": "LTCBTC",
                    "status": "TRADING",
                    "baseAsset": "LTC",
                    "baseAssetPrecision": 8,
                    "quoteAsset": "BTC",
                    "quotePrecision": 8,
                    "quoteAssetPrecision": 8,
                    "baseCommissionPrecision": 8,
                    "quoteCommissionPrecision": 8,
                    "orderTypes": [
                        "LIMIT",
                        "LIMIT_MAKER",
                        "MARKET",
                        "STOP_LOSS_LIMIT",
                        "TAKE_PROFIT_LIMIT"
                    ],
                    "icebergAllowed": True,
                    "ocoAllowed": True,
                    "quoteOrderQtyMarketAllowed": True,
                    "allowTrailingStop": False,
                    "isSpotTradingAllowed": True,
                    "isMarginTradingAllowed": True,
                    "filters": [
                        {
                            "filterType": "PRICE_FILTER",
                            "minPrice": "0.00000100",
                            "maxPrice": "100000.00000000",
                            "tickSize": "0.00000100"
                        },
                        ...
                    ],
                    "permissions": [
                        "SPOT",
                        "MARGIN"
                    ]
                },
                {
                    "symbol": "BNBBTC",
                    "status": "TRADING",
                    "baseAsset": "BNB",
                    "baseAssetPrecision": 8,
                    "quoteAsset": "BTC",
                    "quotePrecision": 8,
                    "quoteAssetPrecision": 8,
                    "baseCommissionPrecision": 8,
                    "quoteCommissionPrecision": 8,
                    "orderTypes": [
                        "LIMIT",
                        "LIMIT_MAKER",
                        "MARKET",
                        "STOP_LOSS_LIMIT",
                        "TAKE_PROFIT_LIMIT"
                    ],
                    "icebergAllowed": True,
                    "ocoAllowed": True,
                    "quoteOrderQtyMarketAllowed": True,
                    "allowTrailingStop": False,
                    "isSpotTradingAllowed": True,
                    "isMarginTradingAllowed": True,
                    "filters": [
                        {
                            "filterType": "PRICE_FILTER",
                            "minPrice": "0.00000100",
                            "maxPrice": "100000.00000000",
                            "tickSize": "0.00000100"
                        },
                        ...
                    ],
                    "permissions": [
                        "SPOT",
                        "MARGIN"
                    ]
                }
            ]
        }
        ```

        Args:
            symbol: if provided will be returned exchange info with specific `symbol`.
            symbols: if provided will be returned exchange info with specific `symbols`.

        Returns:
            Exchange info.

        Raises:
            BinanceInvalidSymbolError: will be raised if `symbol` does not exist
                or symbol in `symbols` does not exist.
        """

        if symbol is not None and symbols is not None:
            raise TypeError(
                "Must be provided only `symbol` or `symbols` argument, not both."
            )

        params = {}
        if symbol is not None:
            params["symbol"] = symbol
        if symbols is not None:
            symbols = [f'"{s}"' for s in symbols]
            symbols_param = ",".join(symbols)
            symbols_param = f"[{symbols_param}]"
            params["symbols"] = symbols_param

        request = Request(
            method="GET",
            base_url=self._base_url,
            path="/api/v3/exchangeInfo",
            params=params,
        )
        response = await self._send_request(request)
        result: BinanceExchangeInfo = response

        return result

    async def get_account_info(
        self, credentials: BinanceCredentials, recv_window: int | None = None
    ) -> BinanceAccountInfo:
        """Returns account info - balances, fees, permissions.

        ```pycon
        >>> import asyncio
        >>> from exapi.exchanges.binance.rest import BinanceRESTWithoutCredentials
        >>> from exapi.exchanges.binance.typedefs import BinanceAccountInfo
        >>>
        >>> async def get_account_info() -> BinanceAccountInfo:
        ...     credentials = BinanceCredentials("API_KEY", "API_SECRET")
        ...     async with BinanceRESTWithoutCredentials() as rest:
        ...         return await rest.get_account_info(credentials)
        ...
        >>> asyncio.run(get_account_info())
        {
            "makerCommission": 15,
            "takerCommission": 15,
            "buyerCommission": 0,
            "sellerCommission": 0,
            "canTrade": True,
            "canWithdraw": True,
            "canDeposit": True,
            "updateTime": 123456789,
            "accountType": "SPOT",
            "balances": [
                {
                    "asset": "BTC",
                    "free": "4723846.89208129",
                    "locked": "0.00000000"
                },
                {
                    "asset": "LTC",
                    "free": "4763368.68006011",
                    "locked": "0.00000000"
                }
            ],
            "permissions": [
                "SPOT"
            ]
        }
        ```

        Args:
            credentials: api keys.
            recv_window: the value cannot be greater than 60000.

        Returns:
            Account info.
        """

        params: dict[str, str] = {}
        if recv_window is not None:
            params["recvWindow"] = str(recv_window)

        request = Request(
            method="GET",
            base_url=self._base_url,
            path="/api/v3/account",
            params=params,
        )
        response = await self._send_private_request(request, credentials)
        result: BinanceAccountInfo = response

        return result

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["MARKET"],
        time_in_force: None = None,
        quantity: str,
        quote_order_qty: None = None,
        price: None = None,
        new_client_order_id: str | None = None,
        stop_price: None = None,
        iceberg_qty: None = None,
        new_order_response_type: Literal["FULL"] | None = None,
        recv_window: int | None = None,
        credentials: BinanceCredentials,
    ) -> BinanceFullOrderResponse:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["MARKET"],
        time_in_force: None = None,
        quantity: None = None,
        quote_order_qty: str,
        price: None = None,
        new_client_order_id: str | None = None,
        stop_price: None = None,
        iceberg_qty: None = None,
        new_order_response_type: Literal["FULL"] | None = None,
        recv_window: int | None = None,
        credentials: BinanceCredentials,
    ) -> BinanceFullOrderResponse:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["MARKET"],
        time_in_force: None = None,
        quantity: str,
        quote_order_qty: None = None,
        price: None = None,
        new_client_order_id: str | None = None,
        stop_price: None = None,
        iceberg_qty: None = None,
        new_order_response_type: Literal["ACK"],
        recv_window: int | None = None,
        credentials: BinanceCredentials,
    ) -> BinanceAckOrderResponse:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["MARKET"],
        time_in_force: None = None,
        quantity: None = None,
        quote_order_qty: str,
        price: None = None,
        new_client_order_id: str | None = None,
        stop_price: None = None,
        iceberg_qty: None = None,
        new_order_response_type: Literal["ACK"],
        recv_window: int | None = None,
        credentials: BinanceCredentials,
    ) -> BinanceAckOrderResponse:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["MARKET"],
        time_in_force: None = None,
        quantity: str,
        quote_order_qty: None = None,
        price: None = None,
        new_client_order_id: str | None = None,
        stop_price: None = None,
        iceberg_qty: None = None,
        new_order_response_type: Literal["RESULT"],
        recv_window: int | None = None,
        credentials: BinanceCredentials,
    ) -> BinanceResultOrderResponse:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["MARKET"],
        time_in_force: None = None,
        quantity: None = None,
        quote_order_qty: str,
        price: None = None,
        new_client_order_id: str | None = None,
        stop_price: None = None,
        iceberg_qty: None = None,
        new_order_response_type: Literal["RESULT"],
        recv_window: int | None = None,
        credentials: BinanceCredentials,
    ) -> BinanceResultOrderResponse:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["LIMIT"],
        time_in_force: BinanceTimeInForce,
        quantity: str,
        quote_order_qty: None = None,
        price: str,
        new_client_order_id: str | None = None,
        stop_price: None = None,
        iceberg_qty: str | None = None,
        new_order_response_type: Literal["FULL"] | None = None,
        recv_window: int | None = None,
        credentials: BinanceCredentials,
    ) -> BinanceFullOrderResponse:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["LIMIT"],
        time_in_force: BinanceTimeInForce,
        quantity: str,
        quote_order_qty: None = None,
        price: str,
        new_client_order_id: str | None = None,
        stop_price: None = None,
        iceberg_qty: str | None = None,
        new_order_response_type: Literal["ACK"],
        recv_window: int | None = None,
        credentials: BinanceCredentials,
    ) -> BinanceAckOrderResponse:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["LIMIT"],
        time_in_force: BinanceTimeInForce,
        quantity: str,
        quote_order_qty: None = None,
        price: str,
        new_client_order_id: str | None = None,
        stop_price: None = None,
        iceberg_qty: str | None = None,
        new_order_response_type: Literal["RESULT"],
        recv_window: int | None = None,
        credentials: BinanceCredentials,
    ) -> BinanceResultOrderResponse:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["STOP_LOSS", "TAKE_PROFIT"],
        time_in_force: None = None,
        quantity: str,
        quote_order_qty: None = None,
        price: None = None,
        new_client_order_id: str | None = None,
        stop_price: str,
        iceberg_qty: None = None,
        new_order_response_type: Literal["ACK"] | None = None,
        recv_window: int | None = None,
        credentials: BinanceCredentials,
    ) -> BinanceAckOrderResponse:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["STOP_LOSS", "TAKE_PROFIT"],
        time_in_force: None = None,
        quantity: str,
        quote_order_qty: None = None,
        price: None = None,
        new_client_order_id: str | None = None,
        stop_price: str,
        iceberg_qty: None = None,
        new_order_response_type: Literal["RESULT"],
        recv_window: int | None = None,
        credentials: BinanceCredentials,
    ) -> BinanceResultOrderResponse:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["STOP_LOSS", "TAKE_PROFIT"],
        time_in_force: None = None,
        quantity: str,
        quote_order_qty: None = None,
        price: None = None,
        new_client_order_id: str | None = None,
        stop_price: str,
        iceberg_qty: None = None,
        new_order_response_type: Literal["FULL"],
        recv_window: int | None = None,
        credentials: BinanceCredentials,
    ) -> BinanceFullOrderResponse:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["STOP_LOSS_LIMIT", "TAKE_PROFIT_LIMIT"],
        time_in_force: BinanceTimeInForce,
        quantity: str,
        quote_order_qty: None = None,
        price: str,
        new_client_order_id: str | None = None,
        stop_price: str,
        iceberg_qty: str | None = None,
        new_order_response_type: Literal["ACK"] | None = None,
        recv_window: int | None = None,
        credentials: BinanceCredentials,
    ) -> BinanceAckOrderResponse:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["STOP_LOSS_LIMIT", "TAKE_PROFIT_LIMIT"],
        time_in_force: BinanceTimeInForce,
        quantity: str,
        quote_order_qty: None = None,
        price: str,
        new_client_order_id: str | None = None,
        stop_price: str,
        iceberg_qty: str | None = None,
        new_order_response_type: Literal["RESULT"],
        recv_window: int | None = None,
        credentials: BinanceCredentials,
    ) -> BinanceResultOrderResponse:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["STOP_LOSS_LIMIT", "TAKE_PROFIT_LIMIT"],
        time_in_force: BinanceTimeInForce,
        quantity: str,
        quote_order_qty: None = None,
        price: str,
        new_client_order_id: str | None = None,
        stop_price: str,
        iceberg_qty: str | None = None,
        new_order_response_type: Literal["FULL"],
        recv_window: int | None = None,
        credentials: BinanceCredentials,
    ) -> BinanceFullOrderResponse:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["LIMIT_MAKER"],
        time_in_force: None = None,
        quantity: str,
        quote_order_qty: None = None,
        price: str,
        new_client_order_id: str | None = None,
        stop_price: None = None,
        iceberg_qty: None = None,
        new_order_response_type: Literal["ACK"] | None = None,
        recv_window: int | None = None,
        credentials: BinanceCredentials,
    ) -> BinanceAckOrderResponse:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["LIMIT_MAKER"],
        time_in_force: None = None,
        quantity: str,
        quote_order_qty: None = None,
        price: str,
        new_client_order_id: str | None = None,
        stop_price: None = None,
        iceberg_qty: None = None,
        new_order_response_type: Literal["RESULT"],
        recv_window: int | None = None,
        credentials: BinanceCredentials,
    ) -> BinanceResultOrderResponse:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["LIMIT_MAKER"],
        time_in_force: None = None,
        quantity: str,
        quote_order_qty: None = None,
        price: str,
        new_client_order_id: str | None = None,
        stop_price: None = None,
        iceberg_qty: None = None,
        new_order_response_type: Literal["FULL"],
        recv_window: int | None = None,
        credentials: BinanceCredentials,
    ) -> BinanceFullOrderResponse:
        ...

    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: BinanceOrderType,
        time_in_force: BinanceTimeInForce | None = None,
        quantity: str | None = None,
        quote_order_qty: str | None = None,
        price: str | None = None,
        new_client_order_id: str | None = None,
        stop_price: str | None = None,
        iceberg_qty: str | None = None,
        new_order_response_type: BinanceOrderResponseType | None = None,
        recv_window: int | None = None,
        credentials: BinanceCredentials,
    ) -> BinanceAckOrderResponse | BinanceResultOrderResponse | BinanceFullOrderResponse:
        """Creates new order.

        ```pycon
        >>> import asyncio
        >>> from exapi.exchanges.binance.rest import BinanceRESTWithoutCredentials
        >>> from exapi.exchanges.binance.typedefs import BinanceFullOrderResponse, BinanceOrderResponseType
        >>>
        >>> async def new_order(resp_type: BinanceOrderResponseType | None = None) -> BinanceFullOrderResponse:
        ...     credentials = BinanceCredentials("API_KEY", "API_SECRET")
        ...     async with BinanceRESTWithoutCredentials() as rest:
        ...         return await rest.new_order(
        ...             symbol="BTCUSDT",
        ...             side="BUY",
        ...             order_type="MARKET",
        ...             quantity="10",
        ...             new_order_response_type=resp_type,
        ...             credentials=credentials
        ...         )
        ...
        >>> asyncio.run(new_order("ACK"))
        {
            "symbol": "BTCUSDT",
            "orderId": 28,
            "orderListId": -1,
            "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
            "transactTime": 1507725176595
        }
        >>> asyncio.run(new_order("RESULT"))
        {
            "symbol": "BTCUSDT",
            "orderId": 28,
            "orderListId": -1,
            "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
            "transactTime": 1507725176595,
            "price": "0.00000000",
            "origQty": "10.00000000",
            "executedQty": "10.00000000",
            "cummulativeQuoteQty": "10.00000000",
            "status": "FILLED",
            "timeInForce": "GTC",
            "type": "MARKET",
            "side": "BUY"
        }
        >>> asyncio.run(new_order("FULL"))
        {
            "symbol": "BTCUSDT",
            "orderId": 28,
            "orderListId": -1,
            "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
            "transactTime": 1507725176595,
            "price": "0.00000000",
            "origQty": "10.00000000",
            "executedQty": "10.00000000",
            "cummulativeQuoteQty": "10.00000000",
            "status": "FILLED",
            "timeInForce": "GTC",
            "type": "MARKET",
            "side": "BUY",
            "fills": [
                {
                    "price": "4000.00000000",
                    "qty": "10.00000000",
                    "commission": "4.00000000",
                    "commissionAsset": "USDT",
                    "tradeId": 56
                }
            ]
        }
        ```

        Args:
            symbol: example: "BTCUSDT".
            side: BUY or SELL.
            order_type: order type: LIMIT, MARKET, etc.
            time_in_force: time in force.
            quantity: quantity of base currency.
            quote_order_qty: quantity of quote currency to spend. Only for MARKET order type.
            price: price of base currency in quote currency.
            new_client_order_id: a unique id among open orders. Automatically generated if not sent.
            stop_price: used with STOP_LOSS, STOP_LOSS_LIMIT, TAKE_PROFIT, and TAKE_PROFIT_LIMIT orders.
            iceberg_qty: used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to create an iceberg order.
            new_order_response_type: set the response JSON. ACK, RESULT, or FULL;
                MARKET and LIMIT order types default to FULL, all other orders default to ACK.
            recv_window: the value cannot be greater than 60000.
            credentials: api keys.

        Returns:
            Info about created or executed order.

        Raises:
            BinanceInvalidSymbolError: will be raised if `symbol` does not exist.
        """

        # Check params combination for each order type
        match order_type:
            case BinanceOrderTypeEnum.MARKET:
                is_valid_params = (
                    (
                        (quantity is not None and quote_order_qty is None)
                        or (quantity is None and quote_order_qty is not None)
                    )
                    and price is None
                    and stop_price is None
                    and iceberg_qty is None
                    and time_in_force is None
                )
            case BinanceOrderTypeEnum.LIMIT:
                is_valid_params = (
                    price is not None
                    and quantity is not None
                    and time_in_force is not None
                    and quote_order_qty is None
                    and stop_price is None
                )
            case BinanceOrderTypeEnum.STOP_LOSS:
                is_valid_params = (
                    quantity is not None
                    and stop_price is not None
                    and price is None
                    and iceberg_qty is None
                    and quote_order_qty is None
                    and time_in_force is None
                )
            case BinanceOrderTypeEnum.STOP_LOSS_LIMIT:
                is_valid_params = (
                    quantity is not None
                    and price is not None
                    and stop_price is not None
                    and time_in_force is not None
                    and quote_order_qty is None
                )
            case BinanceOrderTypeEnum.TAKE_PROFIT:
                is_valid_params = (
                    quantity is not None
                    and stop_price is not None
                    and price is None
                    and iceberg_qty is None
                    and quote_order_qty is None
                    and time_in_force is None
                )
            case BinanceOrderTypeEnum.TAKE_PROFIT_LIMIT:
                is_valid_params = (
                    quantity is not None
                    and price is not None
                    and stop_price is not None
                    and time_in_force is not None
                    and quote_order_qty is None
                )
            case BinanceOrderTypeEnum.LIMIT_MAKER:
                is_valid_params = (
                    quantity is not None
                    and price is not None
                    and stop_price is None
                    and time_in_force is None
                    and quote_order_qty is None
                    and iceberg_qty is None
                )
        if not is_valid_params:
            raise TypeError(
                "Invalid arguments combination. Maybe you skipped mandatory params or pass incompatible with that order type."
            )

        params: dict[str, str] = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
        }
        if time_in_force is not None:
            params["timeInForce"] = time_in_force
        if quantity is not None:
            params["quantity"] = quantity
        if quote_order_qty is not None:
            params["quoteOrderQty"] = quote_order_qty
        if price is not None:
            params["price"] = price
        if new_client_order_id is not None:
            params["newClientOrderId"] = new_client_order_id
        if stop_price is not None:
            params["stopPrice"] = stop_price
        if iceberg_qty is not None:
            params["icebergQty"] = iceberg_qty
        if new_order_response_type is not None:
            params["newOrderRespType"] = new_order_response_type
        if recv_window is not None:
            params["recvWindow"] = str(recv_window)

        request = Request(
            method="POST", base_url=self._base_url, path="/api/v3/order", params=params
        )
        response = await self._send_private_request(request, credentials)
        result: BinanceAckOrderResponse | BinanceResultOrderResponse | BinanceFullOrderResponse = (
            response
        )

        return result

    async def _handle_response(
        self, request: Request, response: aiohttp.ClientResponse
    ) -> Any:
        """Handles response errors.

        Receive JSON from response.

        If response is not successful raises a exception.

        Args:
            response: response object.

        Returns:
            Response with json body.

        Raises:
            BinanceAuthError
            BinanceInvalidSymbolError
            BinanceBadPrecisionError
            BinanceBadRecvWindowError
        """

        result = await response.json(encoding="utf-8")

        if isinstance(result, list) or "code" not in result:
            return result

        response_info = Response(
            status=response.status,
            headers=cast(HeadersType, response.headers),
            body=result,
        )

        codes_to_exceptions: DefaultDict[int, Type[BinanceError]] = DefaultDict(
            lambda: BinanceError
        )
        codes_to_exceptions.update(
            {
                -1002: BinanceAuthError,
                -1022: BinanceAuthError,
                -2014: BinanceAuthError,
                -2015: BinanceAuthError,
                -1111: BinanceBadPrecisionError,
                -1121: BinanceInvalidSymbolError,
                -1131: BinanceBadRecvWindowError,
            }
        )

        code: int = result["code"]
        msg: str = result["msg"]
        Error = codes_to_exceptions[code]
        raise Error(request=request, response=response_info, msg=msg)

    async def _send_private_request(
        self, request: Request, credentials: BinanceCredentials
    ) -> Any:
        request = sign_request(request, credentials)
        return await self._send_request(request)


class BinanceREST:
    """This class is a wrapper around `BinanceRESTWithoutCredentials`.
    It incapsulates account credentials in `__init__` method.
    It can be useful if you need to manage only one account.
    For private methods you don't need to provide credentials in params.
    If you need to manage multiple accounts use `BinanceRESTWithoutCredentials`.
    """

    def __init__(
        self,
        api_key: str = "",
        api_secret: str = "",
        *,
        base_url: str = "https://api.binance.com",
        request_timeout: float | None = None,
    ) -> None:
        self._credentials = BinanceCredentials(api_key, api_secret)
        self._client = BinanceRESTWithoutCredentials(
            base_url=base_url, request_timeout=request_timeout
        )

    @overload
    async def get_ticker(self, symbol: str) -> BinanceSymbolTicker:
        ...

    @overload
    async def get_ticker(self, symbol: None = None) -> list[BinanceSymbolTicker]:
        ...

    async def get_ticker(
        self, symbol: str | None = None
    ) -> BinanceSymbolTicker | list[BinanceSymbolTicker]:
        """Returns `symbol` order book ticker - best ask and bid orders.

        ```pycon
        >>> import asyncio
        >>> from exapi.exchanges.binance.rest import BinanceREST
        >>> from exapi.exchanges.binance.typedefs import BinanceSymbolTicker
        >>>
        >>> async def get_single_ticker(symbol: str) -> BinanceSymbolTicker:
        ...     async with BinanceREST() as rest:
        ...         return await rest.get_ticker(symbol)
        ...
        >>> asyncio.run(get_single_ticker("LTCBTC"))
        {
            "symbol": "LTCBTC",
            "bidPrice": "4.00000000",
            "bidQty": "431.00000000",
            "askPrice": "4.00000200",
            "askQty": "9.00000000"
        }
        >>>
        >>> async def get_all_tickers() -> list[BinanceSymbolTicker]:
        ...     async with BinanceREST() as rest:
        ...         return await rest.get_ticker()
        ...
        >>> asyncio.run(get_all_tickers())
        [
            {
                "symbol": "LTCBTC",
                "bidPrice": "4.00000000",
                "bidQty": "431.00000000",
                "askPrice": "4.00000200",
                "askQty": "9.00000000"
            },
            {
                "symbol": "ETHBTC",
                "bidPrice": "0.07946700",
                "bidQty": "9.00000000",
                "askPrice": "100000.00000000",
                "askQty": "1000.00000000"
            }
        ]
        ```

        Args:
            symbol: format is "BTCUSDT". If None will be returned tickers for all symbols.

        Returns:
            Symbol ticker or all symbol tickers.

        Raises:
            BinanceInvalidSymbolError: will be raised if `symbol` does not exist.
        """

        return await self._client.get_ticker(symbol=symbol)

    @overload
    async def get_exchange_info(
        self, *, symbol: str, symbols: None = None
    ) -> BinanceExchangeInfo:
        ...

    @overload
    async def get_exchange_info(
        self, *, symbol: None = None, symbols: Iterable[str]
    ) -> BinanceExchangeInfo:
        ...

    @overload
    async def get_exchange_info(
        self, *, symbol: None = None, symbols: None = None
    ) -> BinanceExchangeInfo:
        ...

    async def get_exchange_info(
        self, *, symbol: str | None = None, symbols: Iterable[str] | None = None
    ) -> BinanceExchangeInfo:
        """Returns exchange info.

        ```pycon
        >>> import asyncio
        >>> from exapi.exchanges.binance.rest import BinanceREST
        >>> from exapi.exchanges.binance.typedefs import BinanceExchangeInfo
        >>>
        >>> async def get_exchange_info() -> BinanceExchangeInfo:
        ...     async with BinanceREST() as rest:
        ...         return await rest.get_exchange_info()
        ...
        >>> async def get_exchange_info_with_symbol(symbol: str) -> BinanceExchangeInfo:
        ...     async with BinanceREST() as rest:
        ...         return await rest.get_exchange_info(symbol=symbol)
        ...
        >>> async def get_exchange_info_with_symbols(symbols: list[str]) -> BinanceExchangeInfo:
        ...     async with BinanceREST() as rest:
        ...         return await rest.get_exchange_info(symbols=symbols)
        ...
        >>> asyncio.run(get_exchange_info())
        {
            "timezone": "UTC",
            "serverTime": 1647967664330,
            "rateLimits": [
                {
                    "rateLimitType": "REQUEST_WEIGHT",
                    "interval": "MINUTE",
                    "intervalNum": 1,
                    "limit": 1200
                },
                {
                    "rateLimitType": "ORDERS",
                    "interval": "SECOND",
                    "intervalNum": 10,
                    "limit": 50
                },
                {
                    "rateLimitType": "ORDERS",
                    "interval": "DAY",
                    "intervalNum": 1,
                    "limit": 160000
                },
                {
                    "rateLimitType": "RAW_REQUESTS",
                    "interval": "MINUTE",
                    "intervalNum": 5,
                    "limit": 6100
                }
            ],
            "exchangeFilters": [],
            "symbols": [
                {
                    "symbol": "BNBBTC",
                    "status": "TRADING",
                    "baseAsset": "BNB",
                    "baseAssetPrecision": 8,
                    "quoteAsset": "BTC",
                    "quotePrecision": 8,
                    "quoteAssetPrecision": 8,
                    "baseCommissionPrecision": 8,
                    "quoteCommissionPrecision": 8,
                    "orderTypes": [
                        "LIMIT",
                        "LIMIT_MAKER",
                        "MARKET",
                        "STOP_LOSS_LIMIT",
                        "TAKE_PROFIT_LIMIT"
                    ],
                    "icebergAllowed": True,
                    "ocoAllowed": True,
                    "quoteOrderQtyMarketAllowed": True,
                    "allowTrailingStop": False,
                    "isSpotTradingAllowed": True,
                    "isMarginTradingAllowed": True,
                    "filters": [
                        {
                            "filterType": "PRICE_FILTER",
                            "minPrice": "0.00000100",
                            "maxPrice": "100000.00000000",
                            "tickSize": "0.00000100"
                        },
                        {
                            "filterType": "PERCENT_PRICE",
                            "multiplierUp": "5",
                            "multiplierDown": "0.2",
                            "avgPriceMins": 5
                        },
                        {
                            "filterType": "LOT_SIZE",
                            "minQty": "0.00100000",
                            "maxQty": "100000.00000000",
                            "stepSize": "0.00100000"
                        },
                        {
                            "filterType": "MIN_NOTIONAL",
                            "minNotional": "0.00010000",
                            "applyToMarket": True,
                            "avgPriceMins": 5
                        },
                        {
                            "filterType": "ICEBERG_PARTS",
                            "limit": 10
                        },
                        {
                            "filterType": "MARKET_LOT_SIZE",
                            "minQty": "0.00000000",
                            "maxQty": "21800.92779166",
                            "stepSize": "0.00000000"
                        },
                        {
                            "filterType": "MAX_NUM_ORDERS",
                            "maxNumOrders": 200
                        },
                        {
                            "filterType": "MAX_NUM_ALGO_ORDERS",
                            "maxNumAlgoOrders": 5
                        }
                    ],
                    "permissions": [
                        "SPOT",
                        "MARGIN"
                    ]
                }
            ]
        }
        >>> asyncio.run(get_exchange_info_with_symbol("LTCBTC"))
        {
            "timezone": "UTC",
            "serverTime": 1647967664330,
            "rateLimits": [
                {
                    "rateLimitType": "REQUEST_WEIGHT",
                    "interval": "MINUTE",
                    "intervalNum": 1,
                    "limit": 1200
                },
                ...
            ],
            "exchangeFilters": [],
            "symbols": [
                {
                    "symbol": "LTCBTC",
                    "status": "TRADING",
                    "baseAsset": "LTC",
                    "baseAssetPrecision": 8,
                    "quoteAsset": "BTC",
                    "quotePrecision": 8,
                    "quoteAssetPrecision": 8,
                    "baseCommissionPrecision": 8,
                    "quoteCommissionPrecision": 8,
                    "orderTypes": [
                        "LIMIT",
                        "LIMIT_MAKER",
                        "MARKET",
                        "STOP_LOSS_LIMIT",
                        "TAKE_PROFIT_LIMIT"
                    ],
                    "icebergAllowed": True,
                    "ocoAllowed": True,
                    "quoteOrderQtyMarketAllowed": True,
                    "allowTrailingStop": False,
                    "isSpotTradingAllowed": True,
                    "isMarginTradingAllowed": True,
                    "filters": [
                        {
                            "filterType": "PRICE_FILTER",
                            "minPrice": "0.00000100",
                            "maxPrice": "100000.00000000",
                            "tickSize": "0.00000100"
                        },
                        ...
                    ],
                    "permissions": [
                        "SPOT",
                        "MARGIN"
                    ]
                }
            ]
        }
        >>> asyncio.run(get_exchange_info_with_symbols(["LTCBTC", "BNBBTC"]))
        {
            "timezone": "UTC",
            "serverTime": 1647967664330,
            "rateLimits": [
                {
                    "rateLimitType": "REQUEST_WEIGHT",
                    "interval": "MINUTE",
                    "intervalNum": 1,
                    "limit": 1200
                },
                ...
            ],
            "exchangeFilters": [],
            "symbols": [
                {
                    "symbol": "LTCBTC",
                    "status": "TRADING",
                    "baseAsset": "LTC",
                    "baseAssetPrecision": 8,
                    "quoteAsset": "BTC",
                    "quotePrecision": 8,
                    "quoteAssetPrecision": 8,
                    "baseCommissionPrecision": 8,
                    "quoteCommissionPrecision": 8,
                    "orderTypes": [
                        "LIMIT",
                        "LIMIT_MAKER",
                        "MARKET",
                        "STOP_LOSS_LIMIT",
                        "TAKE_PROFIT_LIMIT"
                    ],
                    "icebergAllowed": True,
                    "ocoAllowed": True,
                    "quoteOrderQtyMarketAllowed": True,
                    "allowTrailingStop": False,
                    "isSpotTradingAllowed": True,
                    "isMarginTradingAllowed": True,
                    "filters": [
                        {
                            "filterType": "PRICE_FILTER",
                            "minPrice": "0.00000100",
                            "maxPrice": "100000.00000000",
                            "tickSize": "0.00000100"
                        },
                        ...
                    ],
                    "permissions": [
                        "SPOT",
                        "MARGIN"
                    ]
                },
                {
                    "symbol": "BNBBTC",
                    "status": "TRADING",
                    "baseAsset": "BNB",
                    "baseAssetPrecision": 8,
                    "quoteAsset": "BTC",
                    "quotePrecision": 8,
                    "quoteAssetPrecision": 8,
                    "baseCommissionPrecision": 8,
                    "quoteCommissionPrecision": 8,
                    "orderTypes": [
                        "LIMIT",
                        "LIMIT_MAKER",
                        "MARKET",
                        "STOP_LOSS_LIMIT",
                        "TAKE_PROFIT_LIMIT"
                    ],
                    "icebergAllowed": True,
                    "ocoAllowed": True,
                    "quoteOrderQtyMarketAllowed": True,
                    "allowTrailingStop": False,
                    "isSpotTradingAllowed": True,
                    "isMarginTradingAllowed": True,
                    "filters": [
                        {
                            "filterType": "PRICE_FILTER",
                            "minPrice": "0.00000100",
                            "maxPrice": "100000.00000000",
                            "tickSize": "0.00000100"
                        },
                        ...
                    ],
                    "permissions": [
                        "SPOT",
                        "MARGIN"
                    ]
                }
            ]
        }
        ```

        Args:
            symbol: if provided will be returned exchange info with specific `symbol`.
            symbols: if provided will be returned exchange info with specific `symbols`.

        Returns:
            Exchange info.

        Raises:
            BinanceInvalidSymbolError: will be raised if `symbol` does not exist
                or symbol in `symbols` does not exist.
        """

        return await self._client.get_exchange_info(
            symbol=symbol,  # type: ignore
            symbols=symbols,  # type: ignore
        )

    async def get_account_info(
        self, recv_window: int | None = None
    ) -> BinanceAccountInfo:
        """Returns account info - balances, fees, permissions.

        ```pycon
        >>> import asyncio
        >>> from exapi.exchanges.binance.rest import BinanceREST
        >>> from exapi.exchanges.binance.typedefs import BinanceAccountInfo
        >>>
        >>> async def get_account_info() -> BinanceAccountInfo:
        ...     async with BinanceREST("API_KEY", "API_SECRET") as rest:
        ...         return await rest.get_account_info()
        ...
        >>> asyncio.run(get_account_info())
        {
            "makerCommission": 15,
            "takerCommission": 15,
            "buyerCommission": 0,
            "sellerCommission": 0,
            "canTrade": True,
            "canWithdraw": True,
            "canDeposit": True,
            "updateTime": 123456789,
            "accountType": "SPOT",
            "balances": [
                {
                    "asset": "BTC",
                    "free": "4723846.89208129",
                    "locked": "0.00000000"
                },
                {
                    "asset": "LTC",
                    "free": "4763368.68006011",
                    "locked": "0.00000000"
                }
            ],
            "permissions": [
                "SPOT"
            ]
        }
        ```

        Args:
            recv_window: the value cannot be greater than 60000.

        Returns:
            Account info.
        """

        credentials = self._credentials
        return await self._client.get_account_info(
            credentials=credentials, recv_window=recv_window
        )

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["MARKET"],
        time_in_force: None = None,
        quantity: str,
        quote_order_qty: None = None,
        price: None = None,
        new_client_order_id: str | None = None,
        stop_price: None = None,
        iceberg_qty: None = None,
        new_order_response_type: Literal["FULL"] | None = None,
        recv_window: int | None = None,
    ) -> BinanceFullOrderResponse:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["MARKET"],
        time_in_force: None = None,
        quantity: None = None,
        quote_order_qty: str,
        price: None = None,
        new_client_order_id: str | None = None,
        stop_price: None = None,
        iceberg_qty: None = None,
        new_order_response_type: Literal["FULL"] | None = None,
        recv_window: int | None = None,
    ) -> BinanceFullOrderResponse:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["MARKET"],
        time_in_force: None = None,
        quantity: str,
        quote_order_qty: None = None,
        price: None = None,
        new_client_order_id: str | None = None,
        stop_price: None = None,
        iceberg_qty: None = None,
        new_order_response_type: Literal["ACK"],
        recv_window: int | None = None,
    ) -> BinanceAckOrderResponse:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["MARKET"],
        time_in_force: None = None,
        quantity: None = None,
        quote_order_qty: str,
        price: None = None,
        new_client_order_id: str | None = None,
        stop_price: None = None,
        iceberg_qty: None = None,
        new_order_response_type: Literal["ACK"],
        recv_window: int | None = None,
    ) -> BinanceAckOrderResponse:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["MARKET"],
        time_in_force: None = None,
        quantity: str,
        quote_order_qty: None = None,
        price: None = None,
        new_client_order_id: str | None = None,
        stop_price: None = None,
        iceberg_qty: None = None,
        new_order_response_type: Literal["RESULT"],
        recv_window: int | None = None,
    ) -> BinanceResultOrderResponse:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["MARKET"],
        time_in_force: None = None,
        quantity: None = None,
        quote_order_qty: str,
        price: None = None,
        new_client_order_id: str | None = None,
        stop_price: None = None,
        iceberg_qty: None = None,
        new_order_response_type: Literal["RESULT"],
        recv_window: int | None = None,
    ) -> BinanceResultOrderResponse:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["LIMIT"],
        time_in_force: BinanceTimeInForce,
        quantity: str,
        quote_order_qty: None = None,
        price: str,
        new_client_order_id: str | None = None,
        stop_price: None = None,
        iceberg_qty: str | None = None,
        new_order_response_type: Literal["FULL"] | None = None,
        recv_window: int | None = None,
    ) -> BinanceFullOrderResponse:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["LIMIT"],
        time_in_force: BinanceTimeInForce,
        quantity: str,
        quote_order_qty: None = None,
        price: str,
        new_client_order_id: str | None = None,
        stop_price: None = None,
        iceberg_qty: str | None = None,
        new_order_response_type: Literal["ACK"],
        recv_window: int | None = None,
    ) -> BinanceAckOrderResponse:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["LIMIT"],
        time_in_force: BinanceTimeInForce,
        quantity: str,
        quote_order_qty: None = None,
        price: str,
        new_client_order_id: str | None = None,
        stop_price: None = None,
        iceberg_qty: str | None = None,
        new_order_response_type: Literal["RESULT"],
        recv_window: int | None = None,
    ) -> BinanceResultOrderResponse:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["STOP_LOSS", "TAKE_PROFIT"],
        time_in_force: None = None,
        quantity: str,
        quote_order_qty: None = None,
        price: None = None,
        new_client_order_id: str | None = None,
        stop_price: str,
        iceberg_qty: None = None,
        new_order_response_type: Literal["ACK"] | None = None,
        recv_window: int | None = None,
    ) -> BinanceAckOrderResponse:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["STOP_LOSS", "TAKE_PROFIT"],
        time_in_force: None = None,
        quantity: str,
        quote_order_qty: None = None,
        price: None = None,
        new_client_order_id: str | None = None,
        stop_price: str,
        iceberg_qty: None = None,
        new_order_response_type: Literal["RESULT"],
        recv_window: int | None = None,
    ) -> BinanceResultOrderResponse:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["STOP_LOSS", "TAKE_PROFIT"],
        time_in_force: None = None,
        quantity: str,
        quote_order_qty: None = None,
        price: None = None,
        new_client_order_id: str | None = None,
        stop_price: str,
        iceberg_qty: None = None,
        new_order_response_type: Literal["FULL"],
        recv_window: int | None = None,
    ) -> BinanceFullOrderResponse:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["STOP_LOSS_LIMIT", "TAKE_PROFIT_LIMIT"],
        time_in_force: BinanceTimeInForce,
        quantity: str,
        quote_order_qty: None = None,
        price: str,
        new_client_order_id: str | None = None,
        stop_price: str,
        iceberg_qty: str | None = None,
        new_order_response_type: Literal["ACK"] | None = None,
        recv_window: int | None = None,
    ) -> BinanceAckOrderResponse:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["STOP_LOSS_LIMIT", "TAKE_PROFIT_LIMIT"],
        time_in_force: BinanceTimeInForce,
        quantity: str,
        quote_order_qty: None = None,
        price: str,
        new_client_order_id: str | None = None,
        stop_price: str,
        iceberg_qty: str | None = None,
        new_order_response_type: Literal["RESULT"],
        recv_window: int | None = None,
    ) -> BinanceResultOrderResponse:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["STOP_LOSS_LIMIT", "TAKE_PROFIT_LIMIT"],
        time_in_force: BinanceTimeInForce,
        quantity: str,
        quote_order_qty: None = None,
        price: str,
        new_client_order_id: str | None = None,
        stop_price: str,
        iceberg_qty: str | None = None,
        new_order_response_type: Literal["FULL"],
        recv_window: int | None = None,
    ) -> BinanceFullOrderResponse:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["LIMIT_MAKER"],
        time_in_force: None = None,
        quantity: str,
        quote_order_qty: None = None,
        price: str,
        new_client_order_id: str | None = None,
        stop_price: None = None,
        iceberg_qty: None = None,
        new_order_response_type: Literal["ACK"] | None = None,
        recv_window: int | None = None,
    ) -> BinanceAckOrderResponse:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["LIMIT_MAKER"],
        time_in_force: None = None,
        quantity: str,
        quote_order_qty: None = None,
        price: str,
        new_client_order_id: str | None = None,
        stop_price: None = None,
        iceberg_qty: None = None,
        new_order_response_type: Literal["RESULT"],
        recv_window: int | None = None,
    ) -> BinanceResultOrderResponse:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: Literal["LIMIT_MAKER"],
        time_in_force: None = None,
        quantity: str,
        quote_order_qty: None = None,
        price: str,
        new_client_order_id: str | None = None,
        stop_price: None = None,
        iceberg_qty: None = None,
        new_order_response_type: Literal["FULL"],
        recv_window: int | None = None,
    ) -> BinanceFullOrderResponse:
        ...

    async def new_order(
        self,
        *,
        symbol: str,
        side: BinanceOrderSide,
        order_type: BinanceOrderType,
        time_in_force: BinanceTimeInForce | None = None,
        quantity: str | None = None,
        quote_order_qty: str | None = None,
        price: str | None = None,
        new_client_order_id: str | None = None,
        stop_price: str | None = None,
        iceberg_qty: str | None = None,
        new_order_response_type: BinanceOrderResponseType | None = None,
        recv_window: int | None = None,
    ) -> BinanceAckOrderResponse | BinanceResultOrderResponse | BinanceFullOrderResponse:
        """Creates new order.

        ```pycon
        >>> import asyncio
        >>> from exapi.exchanges.binance.rest import BinanceREST
        >>> from exapi.exchanges.binance.typedefs import BinanceFullOrderResponse, BinanceOrderResponseType
        >>>
        >>> async def new_order(resp_type: BinanceOrderResponseType | None = None) -> BinanceFullOrderResponse:
        ...     async with BinanceREST("API_KEY", "API_SECRET") as rest:
        ...         return await rest.new_order(
        ...             symbol="BTCUSDT",
        ...             side="BUY",
        ...             order_type="MARKET",
        ...             quantity="10",
        ...             new_order_response_type=resp_type
        ...         )
        ...
        >>> asyncio.run(new_order("ACK"))
        {
            "symbol": "BTCUSDT",
            "orderId": 28,
            "orderListId": -1,
            "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
            "transactTime": 1507725176595
        }
        >>> asyncio.run(new_order("RESULT"))
        {
            "symbol": "BTCUSDT",
            "orderId": 28,
            "orderListId": -1,
            "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
            "transactTime": 1507725176595,
            "price": "0.00000000",
            "origQty": "10.00000000",
            "executedQty": "10.00000000",
            "cummulativeQuoteQty": "10.00000000",
            "status": "FILLED",
            "timeInForce": "GTC",
            "type": "MARKET",
            "side": "BUY"
        }
        >>> asyncio.run(new_order("FULL"))
        {
            "symbol": "BTCUSDT",
            "orderId": 28,
            "orderListId": -1,
            "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
            "transactTime": 1507725176595,
            "price": "0.00000000",
            "origQty": "10.00000000",
            "executedQty": "10.00000000",
            "cummulativeQuoteQty": "10.00000000",
            "status": "FILLED",
            "timeInForce": "GTC",
            "type": "MARKET",
            "side": "BUY",
            "fills": [
                {
                    "price": "4000.00000000",
                    "qty": "10.00000000",
                    "commission": "4.00000000",
                    "commissionAsset": "USDT",
                    "tradeId": 56
                }
            ]
        }
        ```

        Args:
            symbol: example: "BTCUSDT".
            side: BUY or SELL.
            order_type: order type: LIMIT, MARKET, etc.
            time_in_force: time in force.
            quantity: quantity of base currency.
            quote_order_qty: quantity of quote currency to spend. Only for MARKET order type.
            price: price of base currency in quote currency.
            new_client_order_id: a unique id among open orders. Automatically generated if not sent.
            stop_price: used with STOP_LOSS, STOP_LOSS_LIMIT, TAKE_PROFIT, and TAKE_PROFIT_LIMIT orders.
            iceberg_qty: used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to create an iceberg order.
            new_order_response_type: set the response JSON. ACK, RESULT, or FULL;
                MARKET and LIMIT order types default to FULL, all other orders default to ACK.
            recv_window: the value cannot be greater than 60000.

        Returns:
            Info about created order.

        Raises:
            BinanceInvalidSymbolError: will be raised if `symbol` does not exist.
        """

        credentials = self._credentials
        return await self._client.new_order(
            symbol=symbol,
            side=side,
            order_type=order_type,  # type: ignore
            time_in_force=time_in_force,  # type: ignore
            quantity=quantity,  # type: ignore
            quote_order_qty=quote_order_qty,  # type: ignore
            price=price,  # type: ignore
            new_client_order_id=new_client_order_id,
            stop_price=stop_price,  # type: ignore
            iceberg_qty=iceberg_qty,  # type: ignore
            new_order_response_type=new_order_response_type,  # type: ignore
            recv_window=recv_window,
            credentials=credentials,
        )

    async def close(self) -> None:
        """Closes session."""

        await self._client.close()

    async def __aenter__(self) -> "BinanceREST":
        self._client = await self._client.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self._client.__aexit__(exc_type, exc_val, exc_tb)
