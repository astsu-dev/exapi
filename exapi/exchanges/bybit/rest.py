from types import TracebackType
from typing import Any, DefaultDict, Type, cast

import aiohttp

from exapi.base.rest import BaseExchangeREST
from exapi.exchanges.bybit.exceptions import BybitError, BybitInvalidSymbolError
from exapi.exchanges.bybit.models import BybitCredentials
from exapi.exchanges.bybit.typedefs import BybitSymbolInfo, BybitWalletBalances
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
        codes_to_exceptions.update({-100011: BybitInvalidSymbolError})
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
