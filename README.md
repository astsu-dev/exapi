# exapi - Exchanges API

## Quick Start

Get symbol ticker from Binance exchange:

```python
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

## Features

### Binance

#### Market data

- [x] Get symbol order book ticker (`get_ticker`)
- [x] Get exchange information (`get_exchange_info`)

#### Spot Account/Trade

- [x] Get account information (`get_account_info`)
- [x] Place order (`new_order`)

### Bybit

#### Market data

- [x] Get symbols (`get_symbols`)
- [ ] Get ticker (`get_ticker`)

#### Account data

- [x] Place order (`new_order`)

#### Wallet data

- [x] Get wallet balance (`get_balances`)

### FTX

#### Markets

- [x] Get markets (`get_markets`)
- [x] Get orderbook (`get_orderbook`)

#### Account

- [ ] Get account information

#### Orders

- [ ] Place order
