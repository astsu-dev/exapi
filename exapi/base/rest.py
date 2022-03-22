import abc
import asyncio
from types import TracebackType
from typing import Any, Type, TypeVar

import aiohttp

from exapi.exceptions import RESTConnectionTimeoutError, RESTNotConnectionError
from exapi.models import Request

T = TypeVar("T", bound="BaseExchangeREST")


class BaseExchangeREST(abc.ABC):
    def __init__(self, *, base_url: str, request_timeout: float | None = None):
        self._request_timeout = (
            aiohttp.ClientTimeout(total=request_timeout)
            if request_timeout is not None
            else request_timeout
        )
        self._base_url = base_url
        self._session = aiohttp.ClientSession(base_url)

    async def _send_request(self, request: Request) -> Any:
        """Makes http request.

        Handles unsuccessful responses.

        Args:
            request: request data

        Returns:
            JSON response
        """

        try:
            response = await self._session.request(
                request.method,
                request.path,
                params=request.params,
                headers=request.headers,
                data=request.data,
                json=request.json,
                timeout=self._request_timeout,
            )
        except aiohttp.ClientConnectionError as e:
            raise RESTNotConnectionError(request=request) from e
        except asyncio.TimeoutError as e:
            raise RESTConnectionTimeoutError(request=request) from e

        async with response:
            return await self._handle_response(request, response)

    async def close(self) -> None:
        """Closes session."""

        await self._session.close()

    @abc.abstractmethod
    async def _handle_response(
        self, request: Request, response: aiohttp.ClientResponse
    ) -> Any:
        """Handles response errors.

        If response is not successful raises a exception.

        Args:
            response: response object.

        Returns:
            Response
        """

    async def __aenter__(self: T) -> T:
        self._session = await self._session.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self._session.__aexit__(exc_type, exc_val, exc_tb)
