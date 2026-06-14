"""
Custom integration to integrate my_ipx800v3 with Home Assistant.

This integration demonstrates best practices for:
- Config flow setup (user, reconfigure, reauth)
- DataUpdateCoordinator pattern for efficient data fetching
- Multiple platform types (sensor, binary_sensor, switch, select, number)
- Service registration and handling
- Device and entity management
- Proper error handling and recovery

For more details about this integration, please refer to:
https://github.com/amg0/ha_ipx800v3

For integration development guidelines:
https://developers.home-assistant.io/docs/creating_integration_manifest
"""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING
from urllib.parse import urlparse

from aiohttp import web

from homeassistant.components import webhook
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_PORT, CONF_SCAN_INTERVAL, CONF_USERNAME, Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.network import get_url
from homeassistant.loader import async_get_loaded_integration

from .api import MyIPX800V3ApiClient
from .const import CONF_AUTOMATIC_PUSH, CONF_WEBHOOK_ID, CONF_WEBHOOK_URL, DEFAULT_SCAN_INTERVAL, DOMAIN, LOGGER
from .coordinator import MyIPX800V3DataUpdateCoordinator
from .data import MyIPX800V3Data
from .service_actions import async_setup_services

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import MyIPX800V3ConfigEntry

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.SENSOR,
    Platform.SWITCH,
]

# This integration is configured via config entries only
CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """
    Set up the integration.

    This is called once at Home Assistant startup to register service actions.
    Service actions must be registered here (not in async_setup_entry) to ensure:
    - Service action validation works correctly
    - Service actions are available even without config entries
    - Helpful error messages are provided

    This is a Silver Quality Scale requirement.

    Args:
        hass: The Home Assistant instance.
        config: The Home Assistant configuration.

    Returns:
        True if setup was successful.

    For more information:
    https://developers.home-assistant.io/docs/dev_101_services
    """
    await async_setup_services(hass)
    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: MyIPX800V3ConfigEntry,
) -> bool:
    """
    Set up this integration using UI.

    This is called when a config entry is loaded. It:
    1. Creates the API client with credentials from the config entry
    2. Initializes the DataUpdateCoordinator for data fetching
    3. Performs the first data refresh
    4. Sets up all platforms (sensors, switches, etc.)
    5. Registers services
    6. Sets up reload listener for config changes

    Data flow in this integration:
    1. User enters username/password in config flow (config_flow.py)
    2. Credentials stored in entry.data[CONF_USERNAME/CONF_PASSWORD]
    3. API Client initialized with credentials (api/client.py)
    4. Coordinator fetches data using authenticated client (coordinator/base.py)
    5. Entities access data via self.coordinator.data (sensor/, binary_sensor/, etc.)

    This pattern ensures credentials from setup flow are used throughout
    the integration's lifecycle for API communication.

    Args:
        hass: The Home Assistant instance.
        entry: The config entry being set up.

    Returns:
        True if setup was successful.

    For more information:
    https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
    """
    # Initialize client first
    client = MyIPX800V3ApiClient(
        host=entry.data[CONF_HOST],
        port=int(entry.data[CONF_PORT]),
        username=entry.data.get(CONF_USERNAME, ""),
        password=entry.data.get(CONF_PASSWORD, ""),
        session=async_get_clientsession(hass),
    )

    # Initialize coordinator with config_entry
    scan_interval = entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

    coordinator = MyIPX800V3DataUpdateCoordinator(
        hass=hass,
        logger=LOGGER,
        name=DOMAIN,
        config_entry=entry,
        update_interval=timedelta(seconds=scan_interval),
        always_update=False,  # Only update entities when data actually changes
    )

    # Register the webhook
    webhook_id = entry.data[CONF_WEBHOOK_ID]
    try:
        webhook.async_register(
            hass,
            DOMAIN,
            "My IPX800V3 Webhook",
            webhook_id,
            handle_webhook,
            allowed_methods=("GET", "POST"),
        )
        LOGGER.debug("Registered webhook with url: %s", entry.data[CONF_WEBHOOK_URL])
    except ValueError:
        LOGGER.warning("Le webhook %s est déjà défini !", webhook_id)

    # Store runtime data
    entry.runtime_data = MyIPX800V3Data(
        client=client,
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    # https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
    await coordinator.async_config_entry_first_refresh()

    # Get the URL string, Parse out just the hostname/IP and the port
    base_url = get_url(hass, allow_external=False)
    parsed_url = urlparse(base_url)
    ip_address = parsed_url.hostname
    port = parsed_url.port  # e.g., 8123

    # Configure the WebHook in the IPX 800
    if entry.data.get(CONF_AUTOMATIC_PUSH, True):
        await client.async_config_push(
            internal_addr=ip_address,
            internal_port=port,
            webhook_url=webhook.async_generate_path(entry.data[CONF_WEBHOOK_ID]),
        )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


# /api/webhook/ipx800-push-MmYtm9wNKiMEr-IButVxB2u5
# 192.168.0.35 8123
# Webhook received data: {'O': '00000011000000000000000000000000', 'I': '00000000000000000000000000000000'}
# IPX800 seems buggy, data received is incomplete ( no analog ), so we trigger a full refresh to get the latest data from the API instead of relying on the webhook payload


async def handle_webhook(hass: HomeAssistant, webhook_id: str, request: web.Request) -> None:
    """Handle incoming webhook calls."""

    # 1. Find the entry associated with this specific webhook_id
    # You can iterate over entries for your domain to find the one matching the ID
    entry = next(
        (entry for entry in hass.config_entries.async_entries(DOMAIN) if entry.data.get(CONF_WEBHOOK_ID) == webhook_id),
        None,
    )

    if not entry or not entry.runtime_data:
        LOGGER.error("Webhook received for unknown entry: %s", webhook_id)
        return None

    # 2. Access the coordinator from runtime_data
    coordinator = entry.runtime_data.coordinator

    # 3. Process the data
    data = dict(request.query)
    LOGGER.debug("Webhook received data: %s", data)

    # 4. Trigger the refresh
    # coordinator.async_set_updated_data(data)
    return await coordinator.async_request_refresh()


async def async_unload_entry(
    hass: HomeAssistant,
    entry: MyIPX800V3ConfigEntry,
) -> bool:
    """
    Unload a config entry.

    This is called when the integration is being removed or reloaded.
    It ensures proper cleanup of:
    - All platform entities
    - Registered services
    - Update listeners

    Args:
        hass: The Home Assistant instance.
        entry: The config entry being unloaded.

    Returns:
        True if unload was successful.

    For more information:
    https://developers.home-assistant.io/docs/config_entries_index/#unloading-entries
    """
    webhook.async_unregister(hass, entry.data[CONF_WEBHOOK_ID])
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: MyIPX800V3ConfigEntry,
) -> None:
    """
    Reload config entry.

    This is called when the integration configuration or options have changed.
    It unloads and then reloads the integration with the new configuration.

    Args:
        hass: The Home Assistant instance.
        entry: The config entry being reloaded.

    For more information:
    https://developers.home-assistant.io/docs/config_entries_index/#reloading-entries
    """
    await hass.config_entries.async_reload(entry.entry_id)
