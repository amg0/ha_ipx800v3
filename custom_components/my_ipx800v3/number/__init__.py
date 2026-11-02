"""Number platform for my_ipx800v3."""

from typing import TYPE_CHECKING

from .target_humidity import ENTITY_DESCRIPTIONS, MyIPX800V3HumidityNumber

# Acts on the device: the coordinator does not limit outbound calls.
PARALLEL_UPDATES = 1

if TYPE_CHECKING:
    from custom_components.my_ipx800v3.data import MyIPX800V3ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


async def async_setup_entry(
    hass: HomeAssistant,
    entry: MyIPX800V3ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the number platform."""
    async_add_entities(
        MyIPX800V3HumidityNumber(entry.runtime_data.coordinator, description) for description in ENTITY_DESCRIPTIONS
    )
