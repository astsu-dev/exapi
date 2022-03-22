import os
import pprint
from unittest import mock

import pytest
from dotenv import load_dotenv

from exapi.exchanges.binance.enums import (
    BinanceOrderSideEnum,
    BinanceOrderTypeEnum,
    BinanceTimeInForceEnum,
)
from exapi.exchanges.binance.exceptions import BinanceError
from exapi.exchanges.binance.models import BinanceCredentials
from exapi.exchanges.binance.rest import BinanceRESTWithoutCredentials

load_dotenv()

credentials = BinanceCredentials(
    api_key=os.getenv("BINANCE_TEST_API_KEY", ""),
    api_secret=os.getenv("BINANCE_TEST_API_SECRET", ""),
)


@pytest.mark.asyncio
async def test_binance_rest_without_credentials_new_market_order_argument_checking() -> None:
    _send_private_request = mock.AsyncMock()
    _send_private_request.return_value = None
    async with BinanceRESTWithoutCredentials() as rest:
        rest._send_private_request = _send_private_request

        await rest.new_order(
            symbol="BTCUSDT",
            side="BUY",
            order_type="MARKET",
            quantity="100",
            credentials=credentials,
        )
        await rest.new_order(
            symbol="BTCUSDT",
            side="BUY",
            order_type="MARKET",
            quote_order_qty="1000000000",
            credentials=credentials,
        )
        await rest.new_order(
            symbol="BTCUSDT",
            side="BUY",
            order_type="MARKET",
            quantity="100",
            new_client_order_id="sdf",
            new_order_response_type="RESULT",
            credentials=credentials,
        )
        with pytest.raises(TypeError):
            await rest.new_order(
                symbol="BTCUSDT",
                side="BUY",
                order_type="MARKET",
                credentials=credentials,
            )
        with pytest.raises(TypeError):
            await rest.new_order(
                symbol="BTCUSDT",
                side="BUY",
                order_type="MARKET",
                quantity="100",
                quote_order_qty="100",
                credentials=credentials,
            )
        with pytest.raises(TypeError):
            await rest.new_order(
                symbol="BTCUSDT",
                side="BUY",
                order_type="MARKET",
                quantity="100",
                price="100",
                credentials=credentials,
            )
        with pytest.raises(TypeError):
            await rest.new_order(
                symbol="BTCUSDT",
                side="BUY",
                order_type="MARKET",
                quantity="100",
                stop_price="100",
                credentials=credentials,
            )
        with pytest.raises(TypeError):
            await rest.new_order(
                symbol="BTCUSDT",
                side="BUY",
                order_type="MARKET",
                quantity="100",
                iceberg_qty="100",
                credentials=credentials,
            )
        with pytest.raises(TypeError):
            await rest.new_order(
                symbol="BTCUSDT",
                side="BUY",
                order_type="MARKET",
                quantity="100",
                time_in_force="GTC",
                credentials=credentials,
            )


@pytest.mark.asyncio
async def test_binance_rest_without_credentials_new_limit_order_argument_checking() -> None:
    _send_private_request = mock.AsyncMock()
    _send_private_request.return_value = None
    async with BinanceRESTWithoutCredentials() as rest:
        rest._send_private_request = _send_private_request

        await rest.new_order(
            symbol="BTCUSDT",
            side="BUY",
            order_type="LIMIT",
            quantity="100",
            price="100",
            time_in_force="GTC",
            credentials=credentials,
        )
        await rest.new_order(
            symbol="BTCUSDT",
            side="BUY",
            order_type="LIMIT",
            quantity="100",
            price="100",
            time_in_force="GTC",
            iceberg_qty="100",
            credentials=credentials,
        )
        await rest.new_order(
            symbol="BTCUSDT",
            side="BUY",
            order_type="LIMIT",
            quantity="100",
            price="100",
            time_in_force="GTC",
            new_client_order_id="sdf",
            new_order_response_type="RESULT",
            credentials=credentials,
        )
        with pytest.raises(TypeError):
            await rest.new_order(
                symbol="BTCUSDT",
                side="BUY",
                order_type="LIMIT",
                credentials=credentials,
            )
        with pytest.raises(TypeError):
            await rest.new_order(
                symbol="BTCUSDT",
                side="BUY",
                order_type="LIMIT",
                quantity="100",
                price="100",
                credentials=credentials,
            )
        with pytest.raises(TypeError):
            await rest.new_order(
                symbol="BTCUSDT",
                side="BUY",
                order_type="LIMIT",
                price="100",
                time_in_force="GTC",
                credentials=credentials,
            )
        with pytest.raises(TypeError):
            await rest.new_order(
                symbol="BTCUSDT",
                side="BUY",
                order_type="LIMIT",
                quantity="100",
                time_in_force="GTC",
                credentials=credentials,
            )
        with pytest.raises(TypeError):
            await rest.new_order(
                symbol="BTCUSDT",
                side="BUY",
                order_type="LIMIT",
                quantity="100",
                price="100",
                time_in_force="GTC",
                stop_price="100",
                credentials=credentials,
            )
        with pytest.raises(TypeError):
            await rest.new_order(
                symbol="BTCUSDT",
                side="BUY",
                order_type="LIMIT",
                quantity="100",
                price="100",
                time_in_force="GTC",
                quote_order_qty="100",
                credentials=credentials,
            )


@pytest.mark.parametrize("order_type", (("STOP_LOSS", "TAKE_PROFIT")))
@pytest.mark.asyncio
async def test_binance_rest_without_credentials_new_stop_loss_and_take_profit_order_argument_checking(
    order_type: str,
) -> None:
    _send_private_request = mock.AsyncMock()
    _send_private_request.return_value = None
    async with BinanceRESTWithoutCredentials() as rest:
        rest._send_private_request = _send_private_request

        await rest.new_order(
            symbol="BTCUSDT",
            side="BUY",
            order_type=order_type,
            quantity="100",
            stop_price="100",
            credentials=credentials,
        )
        await rest.new_order(
            symbol="BTCUSDT",
            side="BUY",
            order_type=order_type,
            quantity="100",
            stop_price="100",
            new_client_order_id="sdf",
            new_order_response_type="RESULT",
            credentials=credentials,
        )
        with pytest.raises(TypeError):
            await rest.new_order(
                symbol="BTCUSDT",
                side="BUY",
                order_type=order_type,
                credentials=credentials,
            )
        with pytest.raises(TypeError):
            await rest.new_order(
                symbol="BTCUSDT",
                side="BUY",
                order_type=order_type,
                quantity="100",
                credentials=credentials,
            )
        with pytest.raises(TypeError):
            await rest.new_order(
                symbol="BTCUSDT",
                side="BUY",
                order_type=order_type,
                stop_price="100",
                credentials=credentials,
            )
        with pytest.raises(TypeError):
            await rest.new_order(
                symbol="BTCUSDT",
                side="BUY",
                order_type=order_type,
                quantity="100",
                stop_price="100",
                price="100",
                credentials=credentials,
            )
        with pytest.raises(TypeError):
            await rest.new_order(
                symbol="BTCUSDT",
                side="BUY",
                order_type=order_type,
                quantity="100",
                stop_price="100",
                quote_order_qty="100",
                credentials=credentials,
            )
        with pytest.raises(TypeError):
            await rest.new_order(
                symbol="BTCUSDT",
                side="BUY",
                order_type=order_type,
                quantity="100",
                stop_price="100",
                iceberg_qty="100",
                credentials=credentials,
            )
        with pytest.raises(TypeError):
            await rest.new_order(
                symbol="BTCUSDT",
                side="BUY",
                order_type=order_type,
                quantity="100",
                stop_price="100",
                time_in_force="GTC",
                credentials=credentials,
            )


@pytest.mark.parametrize("order_type", (("STOP_LOSS_LIMIT", "TAKE_PROFIT_LIMIT")))
@pytest.mark.asyncio
async def test_binance_rest_without_credentials_new_stop_loss_limit_and_take_profit_limit_order_argument_checking(
    order_type: str,
) -> None:
    _send_private_request = mock.AsyncMock()
    _send_private_request.return_value = None
    async with BinanceRESTWithoutCredentials() as rest:
        rest._send_private_request = _send_private_request

        await rest.new_order(
            symbol="BTCUSDT",
            side="BUY",
            order_type=order_type,
            quantity="100",
            price="100",
            stop_price="100",
            time_in_force="GTC",
            credentials=credentials,
        )
        await rest.new_order(
            symbol="BTCUSDT",
            side="BUY",
            order_type=order_type,
            quantity="100",
            price="100",
            stop_price="100",
            time_in_force="GTC",
            new_client_order_id="sdf",
            new_order_response_type="RESULT",
            credentials=credentials,
        )
        with pytest.raises(TypeError):
            await rest.new_order(
                symbol="BTCUSDT",
                side="BUY",
                order_type=order_type,
                credentials=credentials,
            )
        with pytest.raises(TypeError):
            await rest.new_order(
                symbol="BTCUSDT",
                side="BUY",
                order_type=order_type,
                quantity="100",
                price="100",
                stop_price="100",
                credentials=credentials,
            )
        with pytest.raises(TypeError):
            await rest.new_order(
                symbol="BTCUSDT",
                side="BUY",
                order_type=order_type,
                quantity="100",
                price="100",
                time_in_force="GTC",
                credentials=credentials,
            )
        with pytest.raises(TypeError):
            await rest.new_order(
                symbol="BTCUSDT",
                side="BUY",
                order_type=order_type,
                quantity="100",
                stop_price="100",
                time_in_force="GTC",
                credentials=credentials,
            )
        with pytest.raises(TypeError):
            await rest.new_order(
                symbol="BTCUSDT",
                side="BUY",
                order_type=order_type,
                price="100",
                stop_price="100",
                time_in_force="GTC",
                credentials=credentials,
            )
        with pytest.raises(TypeError):
            await rest.new_order(
                symbol="BTCUSDT",
                side="BUY",
                order_type=order_type,
                quantity="100",
                price="100",
                stop_price="100",
                time_in_force="GTC",
                quote_order_qty="100",
                credentials=credentials,
            )


@pytest.mark.asyncio
async def test_binance_rest_without_credentials_new_limit_maker_order_argument_checking() -> None:
    _send_private_request = mock.AsyncMock()
    _send_private_request.return_value = None
    async with BinanceRESTWithoutCredentials() as rest:
        rest._send_private_request = _send_private_request

        await rest.new_order(
            symbol="BTCUSDT",
            side="BUY",
            order_type="LIMIT_MAKER",
            quantity="100",
            price="100",
            credentials=credentials,
        )
        await rest.new_order(
            symbol="BTCUSDT",
            side="BUY",
            order_type="LIMIT_MAKER",
            quantity="100",
            price="100",
            new_client_order_id="sdf",
            new_order_response_type="RESULT",
            credentials=credentials,
        )
        with pytest.raises(TypeError):
            await rest.new_order(
                symbol="BTCUSDT",
                side="BUY",
                order_type="LIMIT_MAKER",
                credentials=credentials,
            )
        with pytest.raises(TypeError):
            await rest.new_order(
                symbol="BTCUSDT",
                side="BUY",
                order_type="LIMIT_MAKER",
                quantity="100",
                credentials=credentials,
            )
        with pytest.raises(TypeError):
            await rest.new_order(
                symbol="BTCUSDT",
                side="BUY",
                order_type="LIMIT_MAKER",
                price="100",
                credentials=credentials,
            )
        with pytest.raises(TypeError):
            await rest.new_order(
                symbol="BTCUSDT",
                side="BUY",
                order_type="LIMIT_MAKER",
                quantity="100",
                price="100",
                stop_price="100",
                credentials=credentials,
            )
        with pytest.raises(TypeError):
            await rest.new_order(
                symbol="BTCUSDT",
                side="BUY",
                order_type="LIMIT_MAKER",
                quantity="100",
                price="100",
                iceberg_qty="100",
                credentials=credentials,
            )
        with pytest.raises(TypeError):
            await rest.new_order(
                symbol="BTCUSDT",
                side="BUY",
                order_type="LIMIT_MAKER",
                quantity="100",
                price="100",
                quote_order_qty="100",
                credentials=credentials,
            )


def error_handler(fn):
    async def wrapper(*args, **kwargs):
        try:
            return await fn(*args, **kwargs)
        except BinanceError as e:
            pprint.pprint(e.response)

    return wrapper


@error_handler
async def binance_rest_without_credentials_new_market_order_with_quote_order_qty() -> None:
    async with BinanceRESTWithoutCredentials() as rest:
        res = await rest.new_order(
            symbol="BTCUSDT",
            side=BinanceOrderSideEnum.BUY,
            order_type=BinanceOrderTypeEnum.MARKET,
            quote_order_qty="10",
            credentials=credentials,
        )
    pprint.pprint(res)


@error_handler
async def binance_rest_without_credentials_new_market_order_with_quantity() -> None:
    async with BinanceRESTWithoutCredentials() as rest:
        res = await rest.new_order(
            symbol="BTCUSDT",
            side=BinanceOrderSideEnum.BUY,
            order_type=BinanceOrderTypeEnum.MARKET,
            quantity="10",
            credentials=credentials,
        )
    pprint.pprint(res)


@error_handler
async def binance_rest_without_credentials_new_limit_order() -> None:
    async with BinanceRESTWithoutCredentials() as rest:
        res = await rest.new_order(
            symbol="BTCUSDT",
            side=BinanceOrderSideEnum.BUY,
            order_type=BinanceOrderTypeEnum.LIMIT,
            quantity="0.00034",
            price="40000",
            time_in_force=BinanceTimeInForceEnum.GTC,
            credentials=credentials,
        )
    pprint.pprint(res)
