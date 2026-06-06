"""Sensor platform for my_ipx800v3."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from custom_components.my_ipx800v3.const import CONF_NAME_FROM_IPX
from custom_components.my_ipx800v3.entity import MyIPX800V3Entity
from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorEntityDescription, SensorStateClass
from homeassistant.const import LIGHT_LUX, PERCENTAGE, UnitOfElectricCurrent, UnitOfTemperature

if TYPE_CHECKING:
    from custom_components.my_ipx800v3.data import MyIPX800V3ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


async def async_setup_entry(
    hass: HomeAssistant,
    entry: MyIPX800V3ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform dynamically based on XML keys."""
    coordinator = entry.runtime_data.coordinator

    entities = []

    # Scan coordinator data keys for "analogX" and "countX" where X is a number
    for key in coordinator.data:
        # Analog inputs
        if key.startswith("analog") and key[6:].isdigit():
            analog_index = int(key[6:])
            name = (
                coordinator.names.get(f"analog{analog_index + 1}") if entry.data.get(CONF_NAME_FROM_IPX) else None
            ) or f"Analog Input {analog_index + 1}"
            entity_description = SensorEntityDescription(key=key, name=name, has_entity_name=True)
            entities.append(
                MyIPX800V3SensorEntity(
                    coordinator=coordinator,
                    entity_description=entity_description,
                    anselect=coordinator.data.get(f"anselect{analog_index}"),
                )
            )
        # Pulse counters
        elif key.startswith("count") and key[5:].isdigit():
            count_index = int(key[5:])
            name = (
                coordinator.names.get(f"counter{count_index + 1}") if entry.data.get(CONF_NAME_FROM_IPX) else None
            ) or f"Counter {count_index + 1}"
            entity_description = SensorEntityDescription(
                key=key,
                name=name,
                has_entity_name=True,
            )
            entities.append(
                MyIPX800V3SensorEntity(
                    coordinator=coordinator,
                    entity_description=entity_description,
                )
            )

    if entities:
        async_add_entities(entities)


class MyIPX800V3SensorEntity(MyIPX800V3Entity, SensorEntity):
    """my_ipx800v3 sensor class."""

    def __init__(
        self,
        coordinator: Any,
        entity_description: SensorEntityDescription,
        anselect: str | None = None,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entity_description)
        self._sensor_key = entity_description.key
        self._anselect = anselect
        self._initialize_sensor(self._sensor_key)

    def _initialize_sensor(self, sensorkey) -> None:
        """Initialize sensor-specific attributes based on the key."""
        if sensorkey.startswith("analog") and self._anselect is not None:
            match self._anselect:
                case "2" | "4" | "6":  # X400T Temperature Sensor
                    self._attr_device_class = SensorDeviceClass.TEMPERATURE
                    self._attr_state_class = SensorStateClass.MEASUREMENT
                    self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
                case "3":  # X400L Lux Sensor
                    self._attr_device_class = SensorDeviceClass.ILLUMINANCE
                    self._attr_state_class = SensorStateClass.MEASUREMENT
                    self._attr_native_unit_of_measurement = LIGHT_LUX
                case "5":  # X400H Sensor
                    self._attr_device_class = SensorDeviceClass.HUMIDITY
                    self._attr_state_class = SensorStateClass.MEASUREMENT
                    self._attr_native_unit_of_measurement = PERCENTAGE
                case "7" | "8" | "9" | "12":  # X400CT Sensor
                    self._attr_device_class = SensorDeviceClass.CURRENT
                    self._attr_state_class = SensorStateClass.MEASUREMENT
                    self._attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
                case "10":  # X200 pH Probe
                    self._attr_device_class = SensorDeviceClass.PH
                    self._attr_state_class = SensorStateClass.MEASUREMENT
                    self._attr_native_unit_of_measurement = "Ph"
                case "11":  # X200 ORP Probe
                    self._attr_device_class = SensorDeviceClass.VOLTAGE
                    self._attr_state_class = SensorStateClass.MEASUREMENT
                    self._attr_native_unit_of_measurement = "mV"

    @property
    def native_value(self) -> float | int | str | None:
        """Return the state of the sensor."""
        val = self.coordinator.data.get(self._sensor_key)
        if val is None:
            return None
        # Analog inputs are expected to be float directly from coordinator
        if self._sensor_key.startswith("analog"):
            return float(val) if val is not None else None
        # Convert to numeric if possible for other sensor types
        try:
            if "." in val:
                return float(val)
            return int(val)
        except ValueError:
            return val
