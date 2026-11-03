"""Tests for IPX800 configuration and options flows."""

from unittest.mock import patch

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.my_ipx800v3.const import CONF_AUTOMATIC_PUSH, CONF_NAME_FROM_IPX, DOMAIN
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_PORT, CONF_SCAN_INTERVAL, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType


async def test_user_flow_creates_entry_after_validating_device(hass: HomeAssistant) -> None:
    """A valid device is checked, then setup and polling options create the entry."""
    with patch(
        "custom_components.my_ipx800v3.config_flow_handler.config_flow.validate_credentials",
        return_value={"config_mac": "AA:BB:CC:DD:EE:FF"},
    ):
        result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": "user"})
        assert result["type"] is FlowResultType.FORM
        assert result["step_id"] == "user"

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_HOST: "127.0.0.1",
                CONF_PORT: 80,
                CONF_USERNAME: "demo",
                CONF_PASSWORD: "secret",
                CONF_NAME_FROM_IPX: False,
                CONF_AUTOMATIC_PUSH: False,
            },
        )
        assert result["type"] is FlowResultType.FORM
        assert result["step_id"] == "options_init"

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_SCAN_INTERVAL: 30},
        )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "IPX800 V3 (127.0.0.1)"
    assert result["data"][CONF_HOST] == "127.0.0.1"
    assert result["data"][CONF_PASSWORD] == "secret"
    assert result["options"][CONF_SCAN_INTERVAL] == 30


async def test_options_flow_updates_scan_interval(
    hass: HomeAssistant,
    init_integration: MockConfigEntry,
) -> None:
    """The options flow saves the selected polling interval."""
    result = await hass.config_entries.options.async_init(init_integration.entry_id)
    assert result["type"] is FlowResultType.FORM

    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        {CONF_SCAN_INTERVAL: 30},
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert init_integration.options[CONF_SCAN_INTERVAL] == 30
