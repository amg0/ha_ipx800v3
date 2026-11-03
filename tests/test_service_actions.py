"""Tests for the integration service actions."""

from typing import Any
from unittest.mock import AsyncMock

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.my_ipx800v3.const import DOMAIN
from custom_components.my_ipx800v3.service_actions import SERVICE_RELOAD_DATA
from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.core import HomeAssistant


def _entity_id_for_ipx_key(hass: HomeAssistant, key: str) -> str:
    """Find an entity ID by its IPX800 data key."""
    return next(state.entity_id for state in hass.states.async_all() if state.attributes.get("ipx_key") == key)


async def test_reload_data_refreshes_the_target_entry(
    hass: HomeAssistant,
    init_integration: MockConfigEntry,
    mock_api: AsyncMock,
) -> None:
    """Reloading a targeted entity refreshes its device and reports the result."""
    mock_api.reset_mock()
    entity_id = _entity_id_for_ipx_key(hass, "analog0")

    response: dict[str, Any] | None = await hass.services.async_call(
        DOMAIN,
        SERVICE_RELOAD_DATA,
        {ATTR_ENTITY_ID: entity_id},
        blocking=True,
        return_response=True,
    )

    assert response is not None
    assert response["status"] == "success"
    assert response["last_update_success"] is True
    assert mock_api.await_count == 1
    assert mock_api.await_args is not None
    assert mock_api.await_args.kwargs["url"].endswith("/globalstatus.xml")
