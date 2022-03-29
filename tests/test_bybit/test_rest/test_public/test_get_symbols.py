import pytest

from exapi.exchanges.bybit.rest import BybitREST, BybitRESTWithoutCredentials


@pytest.mark.asyncio
async def test_bybit_rest_without_credentials_get_symbols() -> None:
    async with BybitRESTWithoutCredentials() as rest:
        result = await rest.get_symbols()
    assert {"name", "baseCurrency", "quoteCurrency"}.issubset(set(result[0]))


@pytest.mark.asyncio
async def test_bybit_rest_get_symbols() -> None:
    async with BybitREST() as rest:
        result = await rest.get_symbols()
    assert {"name", "baseCurrency", "quoteCurrency"}.issubset(set(result[0]))
