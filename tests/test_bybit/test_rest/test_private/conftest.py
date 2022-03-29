import os

import pytest
from dotenv.main import load_dotenv

from exapi.exchanges.bybit.models import BybitCredentials

load_dotenv()


@pytest.fixture(scope="package")
def credentials() -> BybitCredentials:
    return BybitCredentials(
        api_key=os.getenv("BYBIT_TEST_API_KEY", ""),
        api_secret=os.getenv("BYBIT_TEST_API_SECRET", ""),
    )
