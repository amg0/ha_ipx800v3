"""
Custom integration to integrate my_ipx800v3 with Home Assistant.

For more details about this integration, please refer to:
https://github.com/amg0/temp
"""

from typing import TYPE_CHECKING

from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
from homeassistant.loader import async_get_loaded_integration

from .api import MyIPX800V3ApiClient
from .const import DOMAIN
from .coordinator import MyIPX800V3DataUpdateCoordinator
from .data import MyIPX800V3Data
from .service_actions import async_setup_services

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import MyIPX800V3ConfigEntry

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.FAN,
    Platform.NUMBER,
    Platform.SELECT,
    Platform.SENSOR,
    Platform.SWITCH,
]

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """
    Register the service actions.

    Returns:
        True once the actions are registered.

    """
    async_setup_services(hass)
    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: MyIPX800V3ConfigEntry,
) -> bool:
    """
    Set up a config entry.

    Returns:
        True once the coordinator has data and every platform is forwarded.

    """
    client = MyIPX800V3ApiClient(
        username=entry.data[CONF_USERNAME],
        password=entry.data[CONF_PASSWORD],
        session=async_get_clientsession(hass),
    )

    coordinator = MyIPX800V3DataUpdateCoordinator(hass, entry)

    entry.runtime_data = MyIPX800V3Data(
        client=client,
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: MyIPX800V3ConfigEntry,
) -> bool:
    """
    Unload a config entry.

    Returns:
        True if every platform unloaded cleanly.

    """
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
