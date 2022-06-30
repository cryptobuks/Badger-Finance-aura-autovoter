import os

import pytest


@pytest.fixture(autouse=True)
def discord_credentials():
    """Mocked Discord Credentials"""
    os.environ['DISCORD_WEBHOOK_URL'] = "someurl"
