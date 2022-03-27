import pytest

from exapi.exchanges.binance.exceptions import BinanceInvalidSymbolError
from exapi.exchanges.binance.rest import BinanceREST, BinanceRESTWithoutCredentials


@pytest.mark.asyncio
async def test_binance_rest_without_credentials_get_ticker_without_symbol() -> None:
    async with BinanceRESTWithoutCredentials() as rest:
        res = await rest.get_ticker()

    assert isinstance(res, list)
    assert "symbol" in res[0]


@pytest.mark.asyncio
async def test_binance_rest_without_credentials_get_ticker_with_symbol() -> None:
    symbol = "BTCUSDT"
    async with BinanceRESTWithoutCredentials() as rest:
        res = await rest.get_ticker(symbol)

    assert res["symbol"] == symbol


@pytest.mark.asyncio
async def test_binance_rest_without_credentials_get_ticker_with_invalid_symbol() -> None:
    symbol = "INVALID-SYMBOL"
    async with BinanceRESTWithoutCredentials() as rest:
        with pytest.raises(BinanceInvalidSymbolError):
            await rest.get_ticker(symbol)


@pytest.mark.asyncio
async def test_binance_rest_get_ticker_without_symbol() -> None:
    async with BinanceREST() as rest:
        res = await rest.get_ticker()

    assert isinstance(res, list)
    assert "symbol" in res[0]


@pytest.mark.asyncio
async def test_binance_rest_get_ticker_with_symbol() -> None:
    symbol = "BTCUSDT"
    async with BinanceREST() as rest:
        res = await rest.get_ticker(symbol)

    assert res["symbol"] == symbol


@pytest.mark.asyncio
async def test_binance_rest_get_ticker_with_invalid_symbol() -> None:
    symbol = "INVALID-SYMBOL"
    async with BinanceREST() as rest:
        with pytest.raises(BinanceInvalidSymbolError):
            await rest.get_ticker(symbol)
