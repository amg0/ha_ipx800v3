"""Switch platform for my_ipx800v3."""

from typing import TYPE_CHECKING

from .example_switch import ENTITY_DESCRIPTIONS, MyIPX800V3Switch

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
    """Set up the switch platform."""
    async_add_entities(
        MyIPX800V3Switch(entry.runtime_data.coordinator, description) for description in ENTITY_DESCRIPTIONS
    )
