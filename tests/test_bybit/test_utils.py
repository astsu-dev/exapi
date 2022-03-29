from typing import OrderedDict
from unittest import mock

import pytest

from exapi.exchanges.bybit.models import BybitCredentials
from exapi.exchanges.bybit.utils import create_signature, sign_request
from exapi.models import Request


def test_bybit_sign_request_with_get_request_with_empty_params() -> None:
    credentials = BybitCredentials("1tr", "API_SECRET")
    request = Request(method="GET", base_url="url", path="path")
    result = sign_request(request, credentials, timestamp=1234)
    assert result == Request(
        method="GET",
        base_url="url",
        path="path",
        params=OrderedDict(
            api_key="1tr",
            timestamp="1234",
            sign="5259dde2c1f382c7f0a98cc6ac8ffdb1b2ea15a5adbff68d3c8f639fa290af89",
        ),
    )


def test_bybit_sign_request_with_get_request_with_not_empty_params() -> None:
    credentials = BybitCredentials("1tr", "API_SECRET")
    request = Request(
        method="GET", base_url="url", path="path", params={"symbol": "BTCUSDT"}
    )
    result = sign_request(request, credentials, timestamp=1234)
    assert result == Request(
        method="GET",
        base_url="url",
        path="path",
        params=OrderedDict(
            api_key="1tr",
            symbol="BTCUSDT",
            timestamp="1234",
            sign="e2d77eb73ceb5d43600520c542e3fa46fd215c0349addd7b496364220841892e",
        ),
    )


def test_bybit_sign_request_with_post_request_with_empty_data() -> None:
    credentials = BybitCredentials("1tr", "API_SECRET")
    request = Request(method="POST", base_url="url", path="path")
    result = sign_request(request, credentials, timestamp=1234)
    assert result == Request(
        method="POST",
        base_url="url",
        path="path",
        data=OrderedDict(
            api_key="1tr",
            timestamp="1234",
            sign="5259dde2c1f382c7f0a98cc6ac8ffdb1b2ea15a5adbff68d3c8f639fa290af89",
        ),
    )


def test_bybit_sign_request_with_post_request_with_not_empty_data() -> None:
    credentials = BybitCredentials("1tr", "API_SECRET")
    request = Request(
        method="POST", base_url="url", path="path", data={"symbol": "BTCUSDT"}
    )
    result = sign_request(request, credentials, timestamp=1234)
    assert result == Request(
        method="POST",
        base_url="url",
        path="path",
        data=OrderedDict(
            api_key="1tr",
            symbol="BTCUSDT",
            timestamp="1234",
            sign="e2d77eb73ceb5d43600520c542e3fa46fd215c0349addd7b496364220841892e",
        ),
    )


def test_bybit_sign_request_with_not_passed_timestamp() -> None:
    credentials = BybitCredentials("1tr", "API_SECRET")
    request = Request(method="GET", base_url="url", path="path")
    with mock.patch("exapi.exchanges.bybit.utils.get_timestamp") as get_timestamp:
        get_timestamp.return_value = 1234
        result = sign_request(request, credentials)
    assert result == Request(
        method="GET",
        base_url="url",
        path="path",
        params=OrderedDict(
            api_key="1tr",
            timestamp="1234",
            sign="5259dde2c1f382c7f0a98cc6ac8ffdb1b2ea15a5adbff68d3c8f639fa290af89",
        ),
    )


def test_bybit_create_signature() -> None:
    result = create_signature(
        api_secret="API_SECRET", params={"api_key": "1tr", "timestamp": "1234"}
    )
    assert result == "5259dde2c1f382c7f0a98cc6ac8ffdb1b2ea15a5adbff68d3c8f639fa290af89"
