from exapi.exchanges.ftx.models import FTXCredentials
from exapi.exchanges.ftx.utils import create_signature, sign_request
from exapi.models import Request


def test_ftx_create_signature() -> None:
    result = create_signature(
        api_secret="API_SECRET", timestamp=10, method="POST", path="/orders", data="{}"
    )
    assert result == "02e0fbe922c0c48ac2ff60d4c8022d0e109b4bf5a4c1065c2fd8e5b3062146e1"


def test_ftx_sign_request() -> None:
    request = Request(
        method="POST", base_url="https://ftx.com", path="/orders", json={}
    )
    timestamp = 10
    credentials = FTXCredentials("API_KEY", "API_SECRET")
    result = sign_request(request, credentials, timestamp)
    assert result == Request(
        method="POST",
        base_url="https://ftx.com",
        path="/orders",
        headers={
            "FTX-KEY": "API_KEY",
            "FTX-SIGN": "02e0fbe922c0c48ac2ff60d4c8022d0e109b4bf5a4c1065c2fd8e5b3062146e1",
            "FTX-TS": str(timestamp),
        },
        json={},
    )


def test_ftx_sign_request_with_subaccount() -> None:
    request = Request(
        method="POST", base_url="https://ftx.com", path="/orders", json={}
    )
    timestamp = 10
    credentials = FTXCredentials("API_KEY", "API_SECRET", "subaccount")
    result = sign_request(request, credentials, timestamp)
    assert result == Request(
        method="POST",
        base_url="https://ftx.com",
        path="/orders",
        headers={
            "FTX-KEY": "API_KEY",
            "FTX-SIGN": "02e0fbe922c0c48ac2ff60d4c8022d0e109b4bf5a4c1065c2fd8e5b3062146e1",
            "FTX-TS": str(timestamp),
            "FTX-SUBACCOUNT": "subaccount",
        },
        json={},
    )
