from dataclasses import dataclass

from exapi.models import BaseCredentials


@dataclass(frozen=True)
class FTXCredentials(BaseCredentials):
    subaccount: str | None = None
