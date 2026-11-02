"""Binary sensor platform for my_ipx800v3."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from custom_components.my_ipx800v3.binary_sensor.connectivity import (
    CONNECTIVITY_DESCRIPTION,
    MyIPX800V3ConnectivitySensor,
)
from custom_components.my_ipx800v3.const import CONF_NAME_FROM_IPX
from custom_components.my_ipx800v3.entity import MyIPX800V3Entity
from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorEntityDescription

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
    for key in coordinator.data:
        if key.startswith("btn") and key[3:].isdigit():
            input_index = int(key[3:])
            name = (
                coordinator.names.get(f"input{input_index + 1}") if entry.data.get(CONF_NAME_FROM_IPX) else None
            ) or f"Input {input_index + 1}"
            entity_description = BinarySensorEntityDescription(
                key=key,
                name=name,
                has_entity_name=False,
            )
            entities.append(
                MyIPX800V3BinarySensorEntity(
                    coordinator=coordinator,
                    entity_description=entity_description,
                )
            )

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


class MyIPX800V3BinarySensorEntity(MyIPX800V3Entity, BinarySensorEntity):
    """my_ipx800v3 binary_sensor class."""

    def __init__(
        self,
        coordinator: Any,
        entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator, entity_description)
        self._btn_key = entity_description.key

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on (closed/active, returning 'dn')."""
        val = self.coordinator.data.get(self._btn_key)
        return val == "dn"
