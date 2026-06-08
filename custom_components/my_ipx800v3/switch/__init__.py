"""Switch platform for my_ipx800v3."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from custom_components.my_ipx800v3.const import CONF_NAME_FROM_IPX
from custom_components.my_ipx800v3.entity import MyIPX800V3Entity
from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription

if TYPE_CHECKING:
    from custom_components.my_ipx800v3.data import MyIPX800V3ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


async def async_setup_entry(
    hass: HomeAssistant,
    entry: MyIPX800V3ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the switch platform dynamically based on XML keys."""
    coordinator = entry.runtime_data.coordinator

    # Scan coordinator data keys for "ledX" where X is a number
    # GCE IPX800 V3 relays are labeled "led0" to "led31"
    entities = []
    for key in coordinator.data:
        if key.startswith("led") and key[3:].isdigit():
            relay_index = int(key[3:])
            # get name from coordinator if option ('names_from_ipx') is enabled, otherwise default to "Relay X"
            name = (
                coordinator.names.get(f"output{relay_index + 1}") if entry.data.get(CONF_NAME_FROM_IPX) else None
            ) or f"Relay {relay_index + 1}"
            entity_description = SwitchEntityDescription(
                key=key,
                name=name,
                has_entity_name=True,
            )
            entities.append(
                MyIPX800V3SwitchEntity(
                    coordinator=coordinator,
                    entity_description=entity_description,
                    relay_index=relay_index,
                )
            )
        elif key.startswith("btn") and key[3:].isdigit():
            input_index = int(key[3:])
            name = (
                coordinator.names.get(f"input{input_index + 1}") if entry.data.get(CONF_NAME_FROM_IPX) else None
            ) or f"Input {input_index + 1}"
            entity_description = SwitchEntityDescription(
                key=key,
                name=name,
                has_entity_name=True,
            )
            entities.append(
                MyIPX800V3BinarySensorEntity(
                    coordinator=coordinator,
                    entity_description=entity_description,
                    input_index=input_index,
                )
            )
    if entities:
        async_add_entities(entities)


class MyIPX800V3SwitchEntity(MyIPX800V3Entity, SwitchEntity):
    """my_ipx800v3 switch class."""

    def __init__(
        self,
        coordinator: Any,
        entity_description: SwitchEntityDescription,
        relay_index: int,
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator, entity_description)
        self._relay_index = relay_index
        self._led_key = entity_description.key

    @property
    def is_on(self) -> bool | None:
        """Return true if the switch is on."""
        val = self.coordinator.data.get(self._led_key)
        return val == "1"

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        # await self.coordinator.config_entry.runtime_data.client.async_set_relay(
        #     self._relay_index,
        #     True,
        # )
        await self.coordinator.config_entry.runtime_data.client.async_set_relay_switch(self._relay_index)
        # Optimistically update and write state
        self.coordinator.data[self._led_key] = "1"
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        # await self.coordinator.config_entry.runtime_data.client.async_set_relay(
        #     self._relay_index,
        #     False,
        # )
        await self.coordinator.config_entry.runtime_data.client.async_set_relay_switch(self._relay_index)
        # Optimistically update and write state
        self.coordinator.data[self._led_key] = "0"
        self.async_write_ha_state()


class MyIPX800V3BinarySensorEntity(MyIPX800V3Entity, SwitchEntity):
    """my_ipx800v3 binary_sensor class."""

    def __init__(
        self,
        coordinator: Any,
        entity_description: SwitchEntityDescription,
        input_index: int,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator, entity_description)
        self._btn_key = entity_description.key
        self._input_index = input_index

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on (closed/active, returning 'dn')."""
        val = self.coordinator.data.get(self._btn_key)
        return val == "dn"

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        # await self.coordinator.config_entry.runtime_data.client.async_set_relay(
        #     self._relay_index,
        #     True,
        # )
        await self.coordinator.config_entry.runtime_data.client.async_set_relay_switch(100 + self._input_index)
        # Optimistically update and write state
        self.coordinator.data[self._btn_key] = "dn"
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        # await self.coordinator.config_entry.runtime_data.client.async_set_relay(
        #     self._relay_index,
        #     False,
        # )
        await self.coordinator.config_entry.runtime_data.client.async_set_relay_switch(100 + self._input_index)
        # Optimistically update and write state
        self.coordinator.data[self._btn_key] = "up"
        self.async_write_ha_state()
