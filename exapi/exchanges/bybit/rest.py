from types import TracebackType
from typing import Any, DefaultDict, Literal, Type, cast, overload

import aiohttp

from exapi.base.rest import BaseExchangeREST
from exapi.exchanges.bybit.exceptions import (
    BybitAuthError,
    BybitError,
    BybitInsufficientBalanceError,
    BybitInvalidParameterError,
    BybitInvalidPriceDecimalsError,
    BybitInvalidQuantityDecimalsError,
    BybitInvalidSymbolError,
    BybitTooHighPriceError,
    BybitTooHighQuantityError,
    BybitTooLowPriceError,
    BybitTooLowQuantityError,
)
from exapi.exchanges.bybit.models import BybitCredentials
from exapi.exchanges.bybit.typedefs import (
    BybitOrder,
    BybitOrderSide,
    BybitOrderType,
    BybitSymbolInfo,
    BybitSymbolTicker,
    BybitTimeInForce,
    BybitWalletBalances,
)
from exapi.exchanges.bybit.utils import sign_request
from exapi.models import Request, Response
from exapi.typedefs import HeadersType


class BybitRESTWithoutCredentials(BaseExchangeREST):
    """Doesn't incapsulate account credentials.
    For private methods you need to provide credentials in params.
    It can be useful if you need to manage multiple accounts.
    You don't need to create multiple instances for each account.
    """

    def __init__(
        self,
        *,
        base_url: str = "https://api.bybit.com",
        request_timeout: float | None = None,
    ) -> None:
        super().__init__(base_url=base_url, request_timeout=request_timeout)

    async def get_symbols(self) -> list[BybitSymbolInfo]:
        """Returns list of symbols.

        ```python
        >>> import asyncio
        >>> from exapi.exchanges.bybit.rest import BybitRESTWithoutCredentials
        >>> from exapi.exchanges.bybit.typedefs import BybitSymbolInfo
        >>>
        >>> async def get_symbols() -> list[BybitSymbolInfo]:
        ...     async with BybitRESTWithoutCredentials() as rest:
        ...         return await rest.get_symbols()
        ...
        >>> asyncio.run(get_symbols())
        [
            {
                "name": "BTCUSDT",
                "alias": "BTCUSDT",
                "baseCurrency": "BTC",
                "quoteCurrency": "USDT",
                "basePrecision": "0.000001",
                "quotePrecision": "0.01",
                "minTradeQuantity": "0.0001",
                "minTradeAmount": "10",
                "minPricePrecision": "0.01",
                "maxTradeQuantity": "2",
                "maxTradeAmount": "200",
                "category": 1
            },
            {
                "name": "ETHUSDT",
                "alias": "ETHUSDT",
                "baseCurrency": "ETH",
                "quoteCurrency": "USDT",
                "basePrecision": "0.0001",
                "quotePrecision": "0.01",
                "minTradeQuantity": "0.0001",
                "minTradeAmount": "10",
                "minPricePrecision": "0.01",
                "maxTradeQuantity": "2",
                "maxTradeAmount": "200",
                "category": 1
            }
        ]
        ```

        Returns:
            List of symbols.
        """

        request = Request(
            method="GET", base_url=self._base_url, path="/spot/v1/symbols"
        )
        response = await self._send_request(request)

        result: list[BybitSymbolInfo] = response
        return result

    @overload
    async def get_ticker(self, symbol: str) -> BybitSymbolTicker:
        ...

    @overload
    async def get_ticker(self, symbol: None = None) -> list[BybitSymbolTicker]:
        ...

    async def get_ticker(
        self, symbol: str | None = None
    ) -> BybitSymbolTicker | list[BybitSymbolTicker]:
        """
        Returns symbol ticker. If `symbol` is not specified will be returned the tickers for all symbols.

        Args:
            symbol (str | None)

        ```python
        >>> import asyncio
        >>> from exapi.exchanges.bybit.rest import BybitRESTWithoutCredentials
        >>> from exapi.exchanges.bybit.typedefs import BybitSymbolTicker
        >>>
        >>> async def get_ticker(symbol: str | None = None) -> BybitSymbolTicker | list[BybitSymbolTicker]:
        ...     async with BybitRESTWithoutCredentials() as rest:
        ...         return await rest.get_ticker(symbol)
        ...
        >>> asyncio.run(get_ticker("BTCUSDT"))
        {
            "symbol": "BTCUSDT",
            "bidPrice": "50005.12",
            "bidQty": "394",
            "askPrice": "50008",
            "askQty": "0.8001",
            "time": 1620919281808
        }
        >>> asyncio.run(get_ticker())
        [
            {
                "symbol": "BTCUSDT",
                "bidPrice": "50005.12",
                "bidQty": "394",
                "askPrice": "50008",
                "askQty": "0.8001",
                "time": 1620919281808
            },
            {
                "symbol": "ETHUSDT",
                "bidPrice": "2100",
                "bidQty": "394",
                "askPrice": "50008",
                "askQty": "0.8001",
                "time": 1620919281808
            },
        ]
        ```

        Returns:
            Symbol ticker or all symbol tickers.
        """

        if symbol is not None:
            params = {"symbol": symbol}
        else:
            params = {}
        request = Request(
            method="GET",
            base_url=self._base_url,
            path="/spot/quote/v1/ticker/book_ticker",
            params=params,
        )
        response = await self._send_request(request)

        result: BybitSymbolTicker | list[BybitSymbolTicker] = response
        return result

    async def get_balances(self, credentials: BybitCredentials) -> BybitWalletBalances:
        """Returns wallet balances.

        ```python
        >>> import asyncio
        >>> from exapi.exchanges.bybit.models import BybitCredentials
        >>> from exapi.exchanges.bybit.rest import BybitRESTWithoutCredentials
        >>> from exapi.exchanges.bybit.typedefs import BybitWalletBalances
        >>>
        >>> async def get_balances() -> BybitWalletBalances:
        ...     credentials = BybitCredentials("API_KEY", "API_SECRET")
        ...     async with BybitRESTWithoutCredentials() as rest:
        ...         return await rest.get_balances(credentials)
        ...
        >>> asyncio.run(get_balances())
        {
            "balances": [
                {
                    "coin": "USDT",
                    "coinId": "USDT",
                    "coinName": "USDT",
                    "total": "10",
                    "free": "10",
                    "locked": "0"
                }
            ]
        }
        ```

        Args:
            credentials: api keys.

        Returns:
            Wallet balances.
        """

        request = Request(
            method="GET", base_url=self._base_url, path="/spot/v1/account"
        )
        request = sign_request(request, credentials)
        response = await self._send_request(request)

        result: BybitWalletBalances = response
        return result

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BybitOrderSide,
        order_type: Literal["MARKET"],
        quantity: str,
        price: None = None,
        time_in_force: None = None,
        order_link_id: str | None = None,
        credentials: BybitCredentials,
    ) -> BybitOrder:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BybitOrderSide,
        order_type: Literal["LIMIT"],
        quantity: str,
        price: str,
        time_in_force: BybitTimeInForce | None = None,
        order_link_id: str | None = None,
        credentials: BybitCredentials,
    ) -> BybitOrder:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BybitOrderSide,
        order_type: Literal["LIMIT_MAKER"],
        quantity: str,
        price: str,
        time_in_force: None = None,
        order_link_id: str | None = None,
        credentials: BybitCredentials,
    ) -> BybitOrder:
        ...

    async def new_order(
        self,
        *,
        symbol: str,
        side: BybitOrderSide,
        order_type: BybitOrderType,
        quantity: str,
        price: str | None = None,
        time_in_force: BybitTimeInForce | None = None,
        order_link_id: str | None = None,
        credentials: BybitCredentials,
    ) -> BybitOrder:
        """Places a new order.

        ```python
        >>> import asyncio
        >>> from exapi.exchanges.bybit.enums import (
        ...     BybitOrderTypeEnum, BybitOrderSideEnum, BybitTimeInForceEnum
        ... )
        >>> from exapi.exchanges.bybit.rest import BybitRESTWithoutCredentials
        >>> from exapi.exchanges.bybit.models import BybitCredentials
        >>> from exapi.exchanges.bybit.typedefs import BybitOrder
        >>>
        >>> async def new_order() -> BybitOrder:
        ...     credentials = BybitCredentials("API_KEY", "API_SECRET")
        ...     async with BybitRESTWithoutCredentials() as rest:
        ...         return await rest.new_order(
        ...             symbol="BTCUSDT",
        ...             side=BybitOrderSideEnum.BUY,
        ...             order_type=BybitOrderTypeEnum.LIMIT,
        ...             quantity="10",
        ...             price="20000",
        ...             time_in_force=BybitTimeInForceEnum.GTC,
        ...             order_link_id="162073788655749",
        ...             credentials=credentials
        ...         )
        ...
        >>> asyncio.run(new_order())
        {
                "accountId": "1",
                "symbol": "ETHUSDT",
                "symbolName": "ETHUSDT",
                "orderLinkId": "162073788655749",
                "orderId": "889208273689997824",
                "transactTime": "1620737886573",
                "price": "20000",
                "origQty": "10",
                "executedQty": "0",
                "status": "NEW",
                "timeInForce": "GTC",
                "type": "LIMIT",
                "side": "Buy"
        }
        ```

        Args:
            symbol: symbol. Example: "BTCUSDT".
            side: order side.
            order_type: order type.
            quantity: order quantity.
                For market orders: when `side` is "Buy", this is in the quote currency.
                Otherwise, `quantity` is in the base currency.
                For example, on BTCUSDT a `Buy` order is in USDT, otherwise it's in BTC.
                For limit orders, the `quantity` is always in the base currency.)
            price: order price. When the type field is MARKET, the price field is optional.
                When the type field is LIMIT or LIMIT_MAKER, the price field is required
            time_in_force: time in force.
            order_link_id: user generated order id.
            credentials: api keys.

        Returns:
            Order.
        """

        data: dict[str, str] = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "qty": quantity,
        }
        if price is not None:
            data["price"] = price
        if time_in_force is not None:
            data["timeInForce"] = time_in_force
        if order_link_id is not None:
            data["orderLinkId"] = order_link_id

        request = Request(
            method="POST", base_url=self._base_url, path="/spot/v1/order", data=data
        )
        request = sign_request(request, credentials)

        try:
            response = await self._send_request(request)
        except BybitInvalidParameterError as e:
            if e.response.body["ret_msg"] in (
                "Data sent for paramter 'symbol' is not valid.",
                "Data sent for parameter 'symbol' is not valid.",
            ):
                raise BybitInvalidSymbolError(e.request, e.response)
            raise

        result: BybitOrder = response
        return result

    async def _handle_response(
        self, request: Request, response: aiohttp.ClientResponse
    ) -> Any:
        result = await response.json(encoding="utf-8")

        code: int = result["ret_code"]
        if code == 0:
            return result["result"]

        codes_to_exceptions: DefaultDict[int, Type[BybitError]] = DefaultDict(
            lambda: BybitError
        )
        codes_to_exceptions.update(
            {
                -1002: BybitAuthError,
                -1022: BybitAuthError,
                -2014: BybitAuthError,
                -2015: BybitAuthError,
                -1130: BybitInvalidParameterError,
                -1131: BybitInsufficientBalanceError,
                -1132: BybitTooHighPriceError,
                -1133: BybitTooLowPriceError,
                -1134: BybitInvalidPriceDecimalsError,
                -1135: BybitTooHighQuantityError,
                -1136: BybitTooLowQuantityError,
                -1137: BybitInvalidQuantityDecimalsError,
                -1121: BybitInvalidSymbolError,
                -100010: BybitInvalidSymbolError,
                -100011: BybitInvalidSymbolError,
            }
        )
        Error = codes_to_exceptions[code]

        response_info = Response(
            status=response.status,
            headers=cast(HeadersType, response.headers),
            body=result,
        )

        raise Error(request=request, response=response_info)


class BybitREST:
    """This class is a wrapper around `BybitRESTWithoutCredentials`.
    It incapsulates account credentials in `__init__` method.
    It can be useful if you need to manage only one account.
    For private methods you don't need to provide credentials in params.
    If you need to manage multiple accounts use `BybitRESTWithoutCredentials`.
    """

    def __init__(
        self,
        api_key: str = "",
        api_secret: str = "",
        *,
        base_url: str = "https://api.bybit.com",
        request_timeout: float | None = None,
    ) -> None:
        self._credentials = BybitCredentials(api_key, api_secret)
        self._client = BybitRESTWithoutCredentials(
            base_url=base_url, request_timeout=request_timeout
        )

    async def get_symbols(self) -> list[BybitSymbolInfo]:
        """Returns list of symbols.

        ```python
        >>> import asyncio
        >>> from exapi.exchanges.bybit.rest import BybitREST
        >>> from exapi.exchanges.bybit.typedefs import BybitSymbolInfo
        >>>
        >>> async def get_symbols() -> list[BybitSymbolInfo]:
        ...     async with BybitREST() as rest:
        ...         return await rest.get_symbols()
        ...
        >>> asyncio.run(get_symbols())
        [
            {
                "name": "BTCUSDT",
                "alias": "BTCUSDT",
                "baseCurrency": "BTC",
                "quoteCurrency": "USDT",
                "basePrecision": "0.000001",
                "quotePrecision": "0.01",
                "minTradeQuantity": "0.0001",
                "minTradeAmount": "10",
                "minPricePrecision": "0.01",
                "maxTradeQuantity": "2",
                "maxTradeAmount": "200",
                "category": 1
            },
            {
                "name": "ETHUSDT",
                "alias": "ETHUSDT",
                "baseCurrency": "ETH",
                "quoteCurrency": "USDT",
                "basePrecision": "0.0001",
                "quotePrecision": "0.01",
                "minTradeQuantity": "0.0001",
                "minTradeAmount": "10",
                "minPricePrecision": "0.01",
                "maxTradeQuantity": "2",
                "maxTradeAmount": "200",
                "category": 1
            }
        ]
        ```

        Returns:
            List of symbols.
        """

        return await self._client.get_symbols()

    @overload
    async def get_ticker(self, symbol: str) -> BybitSymbolTicker:
        ...

    @overload
    async def get_ticker(self, symbol: None) -> list[BybitSymbolTicker]:
        ...

    async def get_ticker(
        self, symbol: str | None = None
    ) -> BybitSymbolTicker | list[BybitSymbolTicker]:
        """
        ```python
        >>> import asyncio
        >>> from exapi.exchanges.bybit.rest import BybitREST
        >>> from exapi.exchanges.bybit.typedefs import BybitSymbolTicker
        >>>
        >>> async def get_ticker(symbol: str | None = None) -> BybitSymbolTicker | list[BybitSymbolTicker]:
        ...     async with BybitREST("", "") as rest:
        ...         return await rest.get_ticker(symbol)
        ...
        >>> asyncio.run(get_ticker("BTCUSDT"))
        {
            "symbol": "BTCUSDT",
            "bidPrice": "50005.12",
            "bidQty": "394",
            "askPrice": "50008",
            "askQty": "0.8001",
            "time": 1620919281808
        }
        >>> asyncio.run(get_ticker())
        [
            {
                "symbol": "BTCUSDT",
                "bidPrice": "50005.12",
                "bidQty": "394",
                "askPrice": "50008",
                "askQty": "0.8001",
                "time": 1620919281808
            },
            {
                "symbol": "ETHUSDT",
                "bidPrice": "2100",
                "bidQty": "394",
                "askPrice": "50008",
                "askQty": "0.8001",
                "time": 1620919281808
            },
        ]
        ```
        """

        return await self._client.get_ticker(symbol)

    async def get_balances(self) -> BybitWalletBalances:
        """Returns wallet balances.

        ```python
        >>> import asyncio
        >>> from exapi.exchanges.bybit.rest import BybitREST
        >>> from exapi.exchanges.bybit.typedefs import BybitWalletBalances
        >>>
        >>> async def get_balances() -> BybitWalletBalances:
        ...     async with BybitREST("API_KEY", "API_SECRET") as rest:
        ...         return await rest.get_balances()
        ...
        >>> asyncio.run(get_balances())
        {
            "balances": [
                {
                    "coin": "USDT",
                    "coinId": "USDT",
                    "coinName": "USDT",
                    "total": "10",
                    "free": "10",
                    "locked": "0"
                }
            ]
        }
        ```

        Returns:
            Wallet balances.
        """

        return await self._client.get_balances(self._credentials)

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BybitOrderSide,
        order_type: Literal["MARKET"],
        quantity: str,
        price: None = None,
        time_in_force: None = None,
        order_link_id: str | None = None,
    ) -> BybitOrder:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BybitOrderSide,
        order_type: Literal["LIMIT"],
        quantity: str,
        price: str,
        time_in_force: BybitTimeInForce | None = None,
        order_link_id: str | None = None,
    ) -> BybitOrder:
        ...

    @overload
    async def new_order(
        self,
        *,
        symbol: str,
        side: BybitOrderSide,
        order_type: Literal["LIMIT_MAKER"],
        quantity: str,
        price: str,
        time_in_force: None = None,
        order_link_id: str | None = None,
    ) -> BybitOrder:
        ...

    async def new_order(
        self,
        *,
        symbol: str,
        side: BybitOrderSide,
        order_type: BybitOrderType,
        quantity: str,
        price: str | None = None,
        time_in_force: BybitTimeInForce | None = None,
        order_link_id: str | None = None,
    ) -> BybitOrder:
        """Places a new order.

        ```python
        >>> import asyncio
        >>> from exapi.exchanges.bybit.enums import (
        ...     BybitOrderTypeEnum, BybitOrderSideEnum, BybitTimeInForceEnum
        ... )
        >>> from exapi.exchanges.bybit.rest import BybitREST
        >>> from exapi.exchanges.bybit.typedefs import BybitOrder
        >>>
        >>> async def new_order() -> BybitOrder:
        ...     async with BybitREST("API_KEY", "API_SECRET") as rest:
        ...         return await rest.new_order(
        ...             symbol="BTCUSDT",
        ...             side=BybitOrderSideEnum.BUY,
        ...             order_type=BybitOrderTypeEnum.LIMIT,
        ...             quantity="10",
        ...             price="20000",
        ...             time_in_force=BybitTimeInForceEnum.GTC,
        ...             order_link_id="162073788655749",
        ...         )
        ...
        >>> asyncio.run(new_order())
        {
                "accountId": "1",
                "symbol": "ETHUSDT",
                "symbolName": "ETHUSDT",
                "orderLinkId": "162073788655749",
                "orderId": "889208273689997824",
                "transactTime": "1620737886573",
                "price": "20000",
                "origQty": "10",
                "executedQty": "0",
                "status": "NEW",
                "timeInForce": "GTC",
                "type": "LIMIT",
                "side": "Buy"
        }
        ```

        Args:
            symbol: symbol. Example: "BTCUSDT".
            side: order side.
            order_type: order type.
            quantity: order quantity.
                For market orders: when `side` is "Buy", this is in the quote currency.
                Otherwise, `quantity` is in the base currency.
                For example, on BTCUSDT a `Buy` order is in USDT, otherwise it's in BTC.
                For limit orders, the `quantity` is always in the base currency.)
            price: order price. When the type field is MARKET, the price field is optional.
                When the type field is LIMIT or LIMIT_MAKER, the price field is required
            time_in_force: time in force.
            order_link_id: user generated order id.

        Returns:
            Order.
        """

        return await self._client.new_order(
            symbol=symbol,
            side=side,
            order_type=order_type,  # type: ignore
            quantity=quantity,
            price=price,  # type: ignore
            time_in_force=time_in_force,  # type: ignore
            order_link_id=order_link_id,
            credentials=self._credentials,
        )

    async def close(self) -> None:
        """Closes session."""

        await self._client.close()

    async def __aenter__(self) -> "BybitREST":
        self._client = await self._client.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self._client.__aexit__(exc_type, exc_val, exc_tb)
