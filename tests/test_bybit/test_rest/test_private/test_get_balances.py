import pytest

from exapi.exchanges.bybit.models import BybitCredentials
from exapi.exchanges.bybit.rest import BybitREST, BybitRESTWithoutCredentials


@pytest.mark.asyncio
async def test_bybit_rest_without_credentials_get_balances(
    credentials: BybitCredentials,
) -> None:
    async with BybitRESTWithoutCredentials() as rest:
        result = await rest.get_balances(credentials)
    assert {"coin", "free", "locked", "total"}.issubset(set(result["balances"][0]))


@pytest.mark.asyncio
async def test_bybit_rest_get_balances(
    credentials: BybitCredentials,
) -> None:
    async with BybitREST(credentials.api_key, credentials.api_secret) as rest:
        result = await rest.get_balances()
    assert {"coin", "free", "locked", "total"}.issubset(set(result["balances"][0]))
