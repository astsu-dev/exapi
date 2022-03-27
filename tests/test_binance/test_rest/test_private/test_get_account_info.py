import pytest

from exapi.exchanges.binance.models import BinanceCredentials
from exapi.exchanges.binance.rest import BinanceREST, BinanceRESTWithoutCredentials


@pytest.mark.asyncio
async def test_binance_rest_without_credentials_get_account_info(
    credentials: BinanceCredentials,
) -> None:
    async with BinanceRESTWithoutCredentials() as rest:
        result = await rest.get_account_info(credentials)
    assert {"makerCommission", "takerCommission", "balances"}.issubset(set(result))


@pytest.mark.asyncio
async def test_binance_rest_get_account_info(credentials: BinanceCredentials) -> None:
    async with BinanceREST(credentials.api_key, credentials.api_secret) as rest:
        result = await rest.get_account_info()
    assert {"makerCommission", "takerCommission", "balances"}.issubset(set(result))
