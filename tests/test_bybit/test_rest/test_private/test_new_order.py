import pytest
from dotenv import load_dotenv

from exapi.exchanges.bybit.exceptions import (
    BybitAuthError,
    BybitInsufficientBalanceError,
    BybitInvalidPriceDecimalsError,
    BybitInvalidQuantityDecimalsError,
    BybitInvalidSymbolError,
)
from exapi.exchanges.bybit.models import BybitCredentials
from exapi.exchanges.bybit.rest import BybitREST

load_dotenv()


@pytest.mark.asyncio
async def test_bybit_rest_new_limit_order_with_insufficient_balance(
    credentials: BybitCredentials,
) -> None:
    async with BybitREST(credentials.api_key, credentials.api_secret) as rest:
        with pytest.raises(BybitInsufficientBalanceError):
            await rest.new_order(
                symbol="BITUSDT",
                side="Sell",
                order_type="LIMIT",
                quantity="100000",
                price="2.1",
            )


@pytest.mark.asyncio
async def test_bybit_rest_new_limit_order_with_invalid_symbol(
    credentials: BybitCredentials,
) -> None:
    async with BybitREST(credentials.api_key, credentials.api_secret) as rest:
        with pytest.raises(BybitInvalidSymbolError):
            await rest.new_order(
                symbol="INVALIDSYMBOL",
                side="Sell",
                order_type="LIMIT",
                quantity="10",
                price="2.1",
            )


@pytest.mark.asyncio
async def test_bybit_rest_new_limit_order_with_invalid_api_keys() -> None:
    async with BybitREST() as rest:
        with pytest.raises(BybitAuthError):
            await rest.new_order(
                symbol="BITUSDT",
                side="Sell",
                order_type="LIMIT",
                quantity="100000",
                price="2.1",
            )


@pytest.mark.asyncio
async def test_bybit_rest_new_limit_order_with_invalid_api_key(
    credentials: BybitCredentials,
) -> None:
    async with BybitREST(
        credentials.api_key + "invalid", credentials.api_secret
    ) as rest:
        with pytest.raises(BybitAuthError):
            await rest.new_order(
                symbol="BITUSDT",
                side="Sell",
                order_type="LIMIT",
                quantity="10",
                price="2",
            )


@pytest.mark.asyncio
async def test_bybit_rest_new_limit_order_with_invalid_price_decimals(
    credentials: BybitCredentials,
) -> None:
    async with BybitREST(credentials.api_key, credentials.api_secret) as rest:
        with pytest.raises(BybitInvalidPriceDecimalsError):
            await rest.new_order(
                symbol="BITUSDT",
                side="Sell",
                order_type="LIMIT",
                quantity="10",
                price="2.000001",
            )


@pytest.mark.asyncio
async def test_bybit_rest_new_limit_order_with_invalid_quantity_decimals(
    credentials: BybitCredentials,
) -> None:
    async with BybitREST(credentials.api_key, credentials.api_secret) as rest:
        with pytest.raises(BybitInvalidQuantityDecimalsError):
            await rest.new_order(
                symbol="BITUSDT",
                side="Sell",
                order_type="LIMIT",
                quantity="10.11111",
                price="2",
            )
