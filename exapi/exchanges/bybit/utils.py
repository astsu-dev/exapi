import hashlib
import hmac
from typing import OrderedDict, cast
from urllib.parse import urlencode

from exapi.exchanges.bybit.models import BybitCredentials
from exapi.models import Request
from exapi.typedefs import ParamsType
from exapi.utils import get_timestamp


def sign_request(
    request: Request, credentials: BybitCredentials, timestamp: int | None = None
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

    method = request.method
    unordered_params = (
        request.params if method == "GET" else cast(ParamsType, request.data or {})
    )

    unordered_params = {
        **unordered_params,
        "timestamp": str(timestamp),
        "api_key": credentials.api_key,
    }
    params: OrderedDict[str, str] = OrderedDict()
    for k in sorted(unordered_params):
        params[k] = unordered_params[k]

    signature = create_signature(credentials.api_secret, params)
    params["sign"] = signature

    if method == "GET":
        params_result = params
        data_result = request.data
    else:
        params_result = request.params
        data_result = params

    return Request(
        method=method,
        base_url=request.base_url,
        path=request.path,
        params=params_result,
        headers=request.headers,
        data=data_result,
        json=request.json,
    )


def create_signature(api_secret: str, params: ParamsType) -> str:
    """Creates HMAC-SHA256 signature.

    Args:
        api_secret: api secret key.
        params: url params for GET request, body form for POST request.

    Returns:
        Singature
    """

    query_string = urlencode(params)
    key = api_secret.encode("utf-8")
    msg = query_string.encode("utf-8")
    signature = hmac.new(key, msg, hashlib.sha256).hexdigest()

    return signature
