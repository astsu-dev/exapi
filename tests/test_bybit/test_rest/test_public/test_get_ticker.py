import pytest
from exapi.exchanges.bybit.rest import BybitRESTWithoutCredentials, BybitREST
from exapi.exchanges.bybit.exceptions import BybitInvalidSymbolError


@pytest.mark.asyncio
async def test_bybit_rest_without_credentials_get_ticker() -> None:
    async with BybitRESTWithoutCredentials() as rest:
        result = await rest.get_ticker("ETHUSDT")
    assert {"symbol", "bidPrice", "bidQty", "askPrice", "askQty"}.issubset(result)
    assert result["symbol"] == "ETHUSDT"


@pytest.mark.asyncio
async def test_bybit_rest_get_ticker() -> None:
    async with BybitREST() as rest:
        result = await rest.get_ticker("ETHUSDT")
    assert {"symbol", "bidPrice", "bidQty", "askPrice", "askQty"}.issubset(result)
    assert result["symbol"] == "ETHUSDT"


@pytest.mark.asyncio
async def test_bybit_rest_get_ticker_with_invalid_symbol() -> None:
    async with BybitREST() as rest:
        with pytest.raises(BybitInvalidSymbolError):
            result = await rest.get_ticker("INVALID-SYMBOL")


@pytest.mark.asyncio
async def test_bybit_rest_without_credentials_get_ticker_with_invalid_symbol() -> None:
    async with BybitRESTWithoutCredentials() as rest:
        with pytest.raises(BybitInvalidSymbolError):
            result = await rest.get_ticker("INVALID-SYMBOL")
