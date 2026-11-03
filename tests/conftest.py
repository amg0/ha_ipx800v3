"""Shared fixtures for the my_ipx800v3 tests."""

from collections.abc import Generator
import logging
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.my_ipx800v3.const import (
    CONF_AUTOMATIC_PUSH,
    CONF_NAME_FROM_IPX,
    CONF_WEBHOOK_ID,
    CONF_WEBHOOK_URL,
    DOMAIN,
)
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_PORT, CONF_SCAN_INTERVAL, CONF_USERNAME
from homeassistant.core import HomeAssistant

API_DATA = """\
<response>
  <analog0>100</analog0>
  <anselect0>1</anselect0>
  <btn0>dn</btn0>
  <led0>0</led0>
  <count0>10</count0>
  <version>3.05</version>
</response>
"""
API_NAMES = """\
<response>
  <analog1>Analog input</analog1>
  <input1>Digital input</input1>
  <output1>Relay</output1>
  <counter1>Counter</counter1>
</response>
"""


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations: None) -> None:
    """Load custom integrations in every test."""


@pytest.fixture(autouse=True)
def fail_on_deprecation_report(caplog: pytest.LogCaptureFixture) -> Generator[None]:
    """Fail a test when Home Assistant logs a deprecation this integration caused."""
    yield
    reports = [
        message
        for record in [*caplog.get_records("setup"), *caplog.get_records("call")]
        if record.levelno >= logging.WARNING
        and DOMAIN in (message := record.getMessage())
        and message.startswith(("Detected that custom integration", "The deprecated"))
    ]
    assert not reports, "\n".join(reports)


@pytest.fixture
def mock_api() -> Generator[AsyncMock]:
    """Return realistic XML payloads from the mocked IPX800 HTTP layer."""

    async def api_response(*, url: str, **kwargs: Any) -> str:
        if url.endswith("/ioname.xml"):
            return API_NAMES
        if url.endswith("/globalstatus.xml"):
            return API_DATA
        return "<response/>"

    with patch(
        "custom_components.my_ipx800v3.api.client.MyIPX800V3ApiClient._api_wrapper",
        new_callable=AsyncMock,
        side_effect=api_response,
    ) as api_wrapper:
        yield api_wrapper


@pytest.fixture
def config_entry() -> MockConfigEntry:
    """Return a config entry for the integration."""
    return MockConfigEntry(
        domain=DOMAIN,
        title="IPX800",
        unique_id="demo",
        data={
            CONF_HOST: "127.0.0.1",
            CONF_PORT: 80,
            CONF_USERNAME: "demo",
            CONF_PASSWORD: "secret",
            CONF_WEBHOOK_ID: "test-ipx800-webhook",
            CONF_WEBHOOK_URL: "http://localhost/api/webhook/test-ipx800-webhook",
            CONF_NAME_FROM_IPX: False,
            CONF_AUTOMATIC_PUSH: False,
        },
        options={CONF_SCAN_INTERVAL: 60},
    )


@pytest.fixture
async def init_integration(
    hass: HomeAssistant,
    mock_api: AsyncMock,
    config_entry: MockConfigEntry,
) -> MockConfigEntry:
    """Set up the integration from a config entry."""
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    return config_entry
