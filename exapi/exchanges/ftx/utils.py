import hashlib
import hmac
import json
from typing import Mapping

from exapi.exchanges.ftx.models import FTXCredentials
from exapi.models import Request
from exapi.utils import get_timestamp


def sign_request(
    request: Request, credentials: FTXCredentials, timestamp: int | None = None
) -> Request:
    """Signs request with HMAC-SHA256 algorithm.

    For correct sign you need to specify all request parameters in params (query string).

    Args:
        request: request to sign.
        credentials: api keys.
        timestamp: If None will be use now timestamp.

    Returns:
        Signed request.
    """

    if timestamp is None:
        timestamp = get_timestamp()

    body = request.json

    method = request.method
    path = request.path
    body_str = json.dumps(body) if body is not None else ""
    signature = create_signature(
        credentials.api_secret, timestamp, method, path, body_str
    )

    headers: Mapping[str, str] = request.headers or {}
    headers = {
        **headers,
        "FTX-KEY": credentials.api_key,
        "FTX-SIGN": signature,
        "FTX-TS": str(timestamp),
    }
    subaccount = credentials.subaccount
    if subaccount is not None:
        headers["FTX-SUBACCOUNT"] = subaccount

    return Request(
        method=method,
        base_url=request.base_url,
        path=path,
        params=request.params,
        headers=headers,
        data=request.data,
        json=body,
    )


def create_signature(
    api_secret: str, timestamp: int, method: str, path: str, data: str
) -> str:
    """Creates HMAC-SHA256 signature.

    Returns:
        Singature
    """

    key = api_secret.encode("utf-8")
    msg = f"{timestamp}{method}{path}{data}".encode("utf-8")
    signature = hmac.new(key, msg, hashlib.sha256).hexdigest()

    return signature
