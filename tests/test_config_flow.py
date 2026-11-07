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


async def test_reconfigure_flow_preserves_existing_credentials(
    hass: HomeAssistant,
    init_integration: MockConfigEntry,
) -> None:
    """Reconfigure validates with existing credentials and updates settings."""
    with patch(
        "custom_components.my_ipx800v3.config_flow_handler.config_flow.validate_credentials",
        return_value={"config_mac": "demo"},
    ) as mock_validate:
        result = await init_integration.start_reconfigure_flow(hass)
        assert result["type"] is FlowResultType.FORM
        assert result["step_id"] == "reconfigure"

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_NAME_FROM_IPX: True,
                CONF_AUTOMATIC_PUSH: False,
            },
        )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "reconfigure_successful"
    mock_validate.assert_awaited_once_with(
        hass,
        host="127.0.0.1",
        port=80,
        username="demo",
        password="secret",
    )
    assert init_integration.data[CONF_NAME_FROM_IPX] is True
    assert init_integration.data[CONF_PASSWORD] == "secret"


async def test_reauth_flow_updates_credentials(
    hass: HomeAssistant,
    init_integration: MockConfigEntry,
) -> None:
    """Reauthentication flow validates and saves updated credentials."""
    with patch(
        "custom_components.my_ipx800v3.config_flow_handler.config_flow.validate_credentials",
        return_value={"config_mac": "demo"},
    ):
        result = await init_integration.start_reauth_flow(hass)
        assert result["type"] is FlowResultType.FORM
        assert result["step_id"] == "reauth_confirm"

        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_USERNAME: "new_user",
                CONF_PASSWORD: "new_password",
            },
        )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "reauth_successful"
    assert init_integration.data[CONF_USERNAME] == "new_user"
    assert init_integration.data[CONF_PASSWORD] == "new_password"
