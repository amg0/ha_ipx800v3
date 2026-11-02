"""Sensor platform for my_ipx800v3."""

from typing import TYPE_CHECKING

from .air_quality import ENTITY_DESCRIPTIONS as AIR_QUALITY_DESCRIPTIONS
from .diagnostic import ENTITY_DESCRIPTIONS as DIAGNOSTIC_DESCRIPTIONS
from .entity import MyIPX800V3Sensor

# Read-only platform: the coordinator already serializes the fetch.
PARALLEL_UPDATES = 0

if TYPE_CHECKING:
    from custom_components.my_ipx800v3.data import MyIPX800V3ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

ENTITY_DESCRIPTIONS = (*AIR_QUALITY_DESCRIPTIONS, *DIAGNOSTIC_DESCRIPTIONS)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: MyIPX800V3ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        MyIPX800V3Sensor(entry.runtime_data.coordinator, description) for description in ENTITY_DESCRIPTIONS
    )
