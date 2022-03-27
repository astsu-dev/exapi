import os

from dotenv import load_dotenv
import pytest
from exapi.exchanges.binance.models import BinanceCredentials

load_dotenv()


@pytest.fixture(scope="package")
def credentials() -> BinanceCredentials:
    credentials = BinanceCredentials(
        api_key=os.getenv("BINANCE_TEST_API_KEY", ""),
        api_secret=os.getenv("BINANCE_TEST_API_SECRET", ""),
    )
    return credentials
