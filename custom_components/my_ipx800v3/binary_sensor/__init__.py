"""Binary sensor platform for my_ipx800v3."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.my_ipx800v3.binary_sensor.connectivity import (
    CONNECTIVITY_DESCRIPTION,
    MyIPX800V3ConnectivitySensor,
)

if TYPE_CHECKING:
    from custom_components.my_ipx800v3.data import MyIPX800V3ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


async def async_setup_entry(
    hass: HomeAssistant,
    entry: MyIPX800V3ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary_sensor platform dynamically based on XML keys."""
    coordinator = entry.runtime_data.coordinator

    # Scan coordinator data keys for "btnX" where X is a number
    # GCE IPX800 V3 inputs are labeled "btn0" to "btn31"
    entities = []

    # Add connectivity sensor as well
    entities.append(
        MyIPX800V3ConnectivitySensor(
            coordinator=coordinator,
            entity_description=CONNECTIVITY_DESCRIPTION,
            api_endpoint=entry.runtime_data.client.base_url,
        )
    )

    if entities:
        async_add_entities(entities)
