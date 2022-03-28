import pytest

from exapi.exchanges.ftx.rest import FTXRESTWithoutCredentials


@pytest.mark.asyncio
async def test_ftx_rest_without_credentials_get_markets() -> None:
    async with FTXRESTWithoutCredentials() as rest:
        result = await rest.get_markets()
    assert {"name", "baseCurrency", "quoteCurrency"}.issubset(set(result[0]))
