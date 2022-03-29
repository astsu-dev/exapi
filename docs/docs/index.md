# Quick Start

Get symbol ticker from Binance exchange:

```pycon
>>> import asyncio
>>> from exapi.exchanges.binance.rest import BinanceRESTWithoutCredentials
>>> from exapi.exchanges.binance.typedefs import BinanceSymbolTicker
>>>
>>> async def get_single_ticker(symbol: str) -> BinanceSymbolTicker:
...     async with BinanceRESTWithoutCredentials() as rest:
...         return await rest.get_ticker(symbol)
...
>>> asyncio.run(get_single_ticker("LTCBTC"))
{
    "symbol": "LTCBTC",
    "bidPrice": "4.00000000",
    "bidQty": "431.00000000",
    "askPrice": "4.00000200",
    "askQty": "9.00000000"
}
>>>
>>> async def get_all_tickers() -> list[BinanceSymbolTicker]:
...     async with BinanceRESTWithoutCredentials() as rest:
...         return await rest.get_ticker()
...
>>> asyncio.run(get_all_tickers())
[
    {
        "symbol": "LTCBTC",
        "bidPrice": "4.00000000",
        "bidQty": "431.00000000",
        "askPrice": "4.00000200",
        "askQty": "9.00000000"
    },
    {
        "symbol": "ETHBTC",
        "bidPrice": "0.07946700",
        "bidQty": "9.00000000",
        "askPrice": "100000.00000000",
        "askQty": "1000.00000000"
    }
]
```
