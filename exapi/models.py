from dataclasses import dataclass, field
from typing import Any, Literal

from exapi.typedefs import FormType, HeadersType, ParamsType


@dataclass(frozen=True)
class BaseCredentials:
    """Data for auth on exchange."""

    api_key: str
    api_secret: str


@dataclass(frozen=True)
class Request:
    """Data for sending request."""

    method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"]
    base_url: str
    path: str
    params: ParamsType = field(default_factory=dict)
    headers: HeadersType = field(default_factory=dict)
    data: FormType | bytes | str | None = None
    json: list | dict | None = None


@dataclass(frozen=True)
class Response:
    """Info about response.

    Args:
        status: http status code.
        headers: headers.
        body: response body.
    """

    status: int
    headers: HeadersType
    body: Any
