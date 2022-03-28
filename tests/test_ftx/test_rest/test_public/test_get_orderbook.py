import pytest
from exapi.exchanges.ftx.exceptions import FTXInvalidMarketError

from exapi.exchanges.ftx.rest import FTXREST, FTXRESTWithoutCredentials


@pytest.mark.asyncio
async def test_ftx_rest_without_credentials_get_orderbook() -> None:
    async with FTXRESTWithoutCredentials() as rest:
        result = await rest.get_orderbook("BTC/USD")
    assert isinstance(result["asks"][0], tuple)
    assert isinstance(result["bids"][0], tuple)


@pytest.mark.asyncio
async def test_ftx_rest_without_credentials_get_orderbook_with_depth() -> None:
    async with FTXRESTWithoutCredentials() as rest:
        result = await rest.get_orderbook("BTC/USD", depth=1)
    assert len(result["asks"]) == 1
    assert len(result["bids"]) == 1


@pytest.mark.asyncio
async def test_ftx_rest_without_credentials_get_orderbook_with_invalid_market() -> None:
    async with FTXRESTWithoutCredentials() as rest:
        with pytest.raises(FTXInvalidMarketError):
            await rest.get_orderbook("INALID/MARKET")


@pytest.mark.asyncio
async def test_ftx_rest_get_orderbook() -> None:
    async with FTXREST() as rest:
        result = await rest.get_orderbook("BTC/USD")
    assert isinstance(result["asks"][0], tuple)
    assert isinstance(result["bids"][0], tuple)


@pytest.mark.asyncio
async def test_ftx_rest_get_orderbook_with_depth() -> None:
    async with FTXREST() as rest:
        result = await rest.get_orderbook("BTC/USD", depth=1)
    assert len(result["asks"]) == 1
    assert len(result["bids"]) == 1


@pytest.mark.asyncio
async def test_ftx_rest_get_orderbook_with_invalid_market() -> None:
    async with FTXREST() as rest:
        with pytest.raises(FTXInvalidMarketError):
            await rest.get_orderbook("INALID/MARKET")
