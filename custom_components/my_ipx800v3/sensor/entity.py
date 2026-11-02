"""Sensor entity for my_ipx800v3."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from custom_components.my_ipx800v3.entity import MyIPX800V3Entity
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.helpers.typing import StateType


@dataclass(frozen=True, kw_only=True)
class MyIPX800V3SensorEntityDescription(SensorEntityDescription):
    """Describes a sensor and how to read it from coordinator data."""

    value_fn: Callable[[dict[str, Any]], StateType]


class MyIPX800V3Sensor(SensorEntity, MyIPX800V3Entity):
    """Sensor backed by one value in the coordinator payload."""

    entity_description: MyIPX800V3SensorEntityDescription

    @property
    def native_value(self) -> StateType:
        """Return the value read from coordinator data."""
        return self.entity_description.value_fn(self.coordinator.data)
