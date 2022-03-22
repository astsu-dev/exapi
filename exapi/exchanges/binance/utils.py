import hashlib
import hmac
from typing import Mapping, OrderedDict
from urllib.parse import urlencode

from exapi.models import Request
from exapi.utils import get_timestamp
from exapi.exchanges.binance.models import BinanceCredentials


def sign_request(
    request: Request, credentials: BinanceCredentials, timestamp: int | None = None
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

    params: Mapping[str, str] = request.params or {}
    headers: Mapping[str, str] = request.headers or {}
    if timestamp is None:
        timestamp = get_timestamp()

    headers = {**headers, "X-MBX-APIKEY": credentials.api_key}
    params = OrderedDict(**params, timestamp=str(timestamp))
    signature = create_signature(credentials.api_secret, params)
    params = OrderedDict(**params, signature=signature)

    return Request(
        method=request.method,
        base_url=request.base_url,
        path=request.path,
        params=params,
        headers=headers,
        data=request.data,
        json=request.json,
    )


def create_signature(api_secret: str, params: Mapping[str, str]) -> str:
    """Creates HMAC-SHA256 signature.

    Returns:
        Singature
    """

    query_string = urlencode(params)
    key = api_secret.encode("utf-8")
    msg = query_string.encode("utf-8")
    signature = hmac.new(key=key, msg=msg, digestmod=hashlib.sha256).hexdigest()

    return signature
