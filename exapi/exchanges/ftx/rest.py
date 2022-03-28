from types import TracebackType
from typing import Any, Type, cast

import aiohttp

from exapi.base.rest import BaseExchangeREST
from exapi.exchanges.ftx.exceptions import FTXError, FTXInvalidMarketError
from exapi.exchanges.ftx.models import FTXCredentials
from exapi.exchanges.ftx.typedefs import FTXMarket
from exapi.models import Request, Response
from exapi.typedefs import HeadersType


class FTXRESTWithoutCredentials(BaseExchangeREST):
    """Doesn't incapsulate account credentials.
    For private methods you need to provide credentials in params.
    It can be useful if you need to manage multiple accounts.
    You don't need to create multiple instances for each account.
    """

    def __init__(
        self,
        *,
        base_url: str = "https://ftx.com",
        request_timeout: float | None = None,
    ) -> None:
        super().__init__(base_url=base_url, request_timeout=request_timeout)

    async def get_markets(self) -> list[FTXMarket]:
        """Returns list of markets.

        >>> import asyncio
        >>> from exapi.exchanges.ftx.rest import FTXRESTWithoutCredentials
        >>>
        >>> async def get_markets() -> list[FTXMarket]:
        ...     async with FTXRESTWithoutCredentials() as rest:
        ...         return await rest.get_markets()
        ...
        >>> asyncio.run(get_markets())
        [
            {
                "name": "BTC-PERP",
                "baseCurrency": None,
                "quoteCurrency": None,
                "quoteVolume24h": 28914.76,
                "change1h": 0.012,
                "change24h": 0.0299,
                "changeBod": 0.0156,
                "highLeverageFeeExempt": False,
                "minProvideSize": 0.001,
                "type": "future",
                "underlying": "BTC",
                "enabled": True,
                "ask": 3949.25,
                "bid": 3949,
                "last": 10579.52,
                "postOnly": False,
                "price": 10579.52,
                "priceIncrement": 0.25,
                "sizeIncrement": 0.0001,
                "restricted": False,
                "volumeUsd24h": 28914.76,
                "largeOrderThreshold": 5000
            }
        ]

        Returns:
            List of markets.
        """

        request = Request(method="GET", base_url=self._base_url, path="/api/markets")
        response = await self._send_request(request)
        result: list[FTXMarket] = response
        return result

    async def _handle_response(
        self, request: Request, response: aiohttp.ClientResponse
    ) -> Any:
        result = await response.json(encoding="utf-8")

        if result["success"]:
            return result["result"]

        response_info = Response(
            status=response.status,
            headers=cast(HeadersType, response.headers),
            body=result,
        )

        error: str = result["error"].lower()
        if error.startswith("no such market"):
            raise FTXInvalidMarketError(request=request, response=response_info)
        raise FTXError(request=request, response=response_info)


class FTXREST:
    """This class is a wrapper around `FTXRESTWithoutCredentials`.
    It incapsulates account credentials in `__init__` method.
    It can be useful if you need to manage only one account.
    For private methods you don't need to provide credentials in params.
    If you need to manage multiple accounts use `FTXRESTWithoutCredentials`.
    """

    def __init__(
        self,
        api_key: str = "",
        api_secret: str = "",
        subaccount: str | None = None,
        *,
        base_url: str = "https://ftx.com",
        request_timeout: float | None = None,
    ) -> None:
        self._credentials = FTXCredentials(api_key, api_secret, subaccount)
        self._client = FTXRESTWithoutCredentials(
            base_url=base_url, request_timeout=request_timeout
        )

    async def get_markets(self) -> list[FTXMarket]:
        """Returns list of markets.

        >>> import asyncio
        >>> from exapi.exchanges.ftx.rest import FTXREST
        >>>
        >>> async def get_markets() -> list[FTXMarket]:
        ...     async with FTXREST() as rest:
        ...         return await rest.get_markets()
        ...
        >>> asyncio.run(get_markets())
        [
            {
                "name": "BTC-PERP",
                "baseCurrency": None,
                "quoteCurrency": None,
                "quoteVolume24h": 28914.76,
                "change1h": 0.012,
                "change24h": 0.0299,
                "changeBod": 0.0156,
                "highLeverageFeeExempt": False,
                "minProvideSize": 0.001,
                "type": "future",
                "underlying": "BTC",
                "enabled": True,
                "ask": 3949.25,
                "bid": 3949,
                "last": 10579.52,
                "postOnly": False,
                "price": 10579.52,
                "priceIncrement": 0.25,
                "sizeIncrement": 0.0001,
                "restricted": False,
                "volumeUsd24h": 28914.76,
                "largeOrderThreshold": 5000
            }
        ]

        Returns:
            List of markets.
        """

        return await self._client.get_markets()

    async def close(self) -> None:
        """Closes session."""

        await self._client.close()

    async def __aenter__(self) -> "FTXREST":
        self._client = await self._client.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self._client.__aexit__(exc_type, exc_val, exc_tb)
