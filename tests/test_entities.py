"""Tests for IPX800 entities."""

from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant.core import HomeAssistant, State


def _state_for_ipx_key(hass: HomeAssistant, key: str) -> State | None:
    """Find an entity state by its IPX800 data key."""
    return next(
        (state for state in hass.states.async_all() if state.attributes.get("ipx_key") == key),
        None,
    )


async def test_entities_expose_coordinator_data(
    hass: HomeAssistant,
    init_integration: MockConfigEntry,
) -> None:
    """Input, relay, analog, counter, and connectivity states reflect the fetched data."""
    analog = _state_for_ipx_key(hass, "analog0")
    digital_input = _state_for_ipx_key(hass, "btn0")
    relay = _state_for_ipx_key(hass, "led0")
    counter = _state_for_ipx_key(hass, "count0")
    connectivity = _state_for_ipx_key(hass, "api_connectivity")

    assert analog is not None
    assert analog.state == "0.323"
    assert digital_input is not None
    assert digital_input.state == "on"
    assert relay is not None
    assert relay.state == "off"
    assert counter is not None
    assert counter.state == "10"
    assert connectivity is not None
    assert connectivity.state == "on"
