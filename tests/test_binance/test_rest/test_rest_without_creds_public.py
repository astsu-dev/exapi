import pytest
from exapi.exchanges.binance.exceptions import BinanceInvalidSymbolError

from exapi.exchanges.binance.rest import BinanceRESTWithoutCredentials


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
async def test_binance_rest_without_credentials_get_exchange_info() -> None:
    async with BinanceRESTWithoutCredentials() as rest:
        res = await rest.get_exchange_info()

    assert {"exchangeFilters", "symbols"}.issubset(set(res))


@pytest.mark.asyncio
async def test_binance_rest_without_credentials_get_exchange_info_with_symbol() -> None:
    symbol = "BTCUSDT"
    async with BinanceRESTWithoutCredentials() as rest:
        res = await rest.get_exchange_info(symbol=symbol)

    assert {"exchangeFilters", "symbols"}.issubset(set(res))
    assert res["symbols"][0]["symbol"] == symbol


@pytest.mark.asyncio
async def test_binance_rest_without_credentials_get_exchange_info_with_invalid_symbol() -> None:
    symbol = "INVALID-SYMBOL"
    async with BinanceRESTWithoutCredentials() as rest:
        with pytest.raises(BinanceInvalidSymbolError):
            await rest.get_exchange_info(symbol=symbol)


@pytest.mark.asyncio
async def test_binance_rest_without_credentials_get_exchange_info_with_symbols() -> None:
    symbols = ("BTCUSDT", "ETHUSDT")
    async with BinanceRESTWithoutCredentials() as rest:
        res = await rest.get_exchange_info(symbols=symbols)

    assert {"exchangeFilters", "symbols"}.issubset(set(res))
    assert res["symbols"][0]["symbol"] in symbols
    assert res["symbols"][1]["symbol"] in symbols


@pytest.mark.asyncio
async def test_binance_rest_without_credentials_get_exchange_info_with_invalid_symbols() -> None:
    symbols = ("BTCUSDT", "INVALID-SYMBOL")
    async with BinanceRESTWithoutCredentials() as rest:
        with pytest.raises(BinanceInvalidSymbolError):
            await rest.get_exchange_info(symbols=symbols)
