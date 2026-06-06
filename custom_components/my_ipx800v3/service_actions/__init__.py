"""Service actions package for my_ipx800v3."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from custom_components.my_ipx800v3.const import DOMAIN, LOGGER
from custom_components.my_ipx800v3.service_actions.example_service import (
    async_handle_example_action,
    async_handle_reload_data,
)
from homeassistant.core import ServiceCall, ServiceResponse, SupportsResponse
from homeassistant.helpers import device_registry as dr, target as target_helpers

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

# Service action names - only used within service_actions module
SERVICE_EXAMPLE_ACTION = "example_action"
SERVICE_RELOAD_DATA = "reload_data"


async def async_setup_services(hass: HomeAssistant) -> None:
    """
    Register services for the integration.

    Services are registered at component level (in async_setup) rather than
    per config entry. This is a Silver Quality Scale requirement and ensures:
    - Service validation works correctly
    - Services are available even without config entries
    - Helpful error messages are provided

    Service handlers iterate over all config entries to find the relevant one.
    """

    async def handle_example_action(call: ServiceCall) -> None:
        """Handle the example_action service call."""
        # Find all config entries for this domain
        entries = hass.config_entries.async_entries(DOMAIN)
        if not entries:
            LOGGER.warning("No config entries found for %s", DOMAIN)
            return

        # Use first entry (or implement logic to select specific entry)
        entry = entries[0]
        await async_handle_example_action(hass, entry, call)

    async def handle_reload_data(call: ServiceCall) -> ServiceResponse:
        """Handle the reload_data service call."""
        # 1. extract target selection from service call data
        target_selection = target_helpers.TargetSelection(call.data)
        device_registry = dr.async_get(hass)
        processed_entries: dict[str, Any] = {}

        # 2. find the proper ConfigEntry for each device_id in the target selection
        for device_id in target_selection.device_ids:
            device_entry = device_registry.async_get(device_id)

            if device_entry:
                # make sure we find the config entry for our domain - a device could be linked to multiple entries from different integrations
                # device store in attribute `config_entries` (a set of IDs)
                target_config_entry = None
                for entry_id in device_entry.config_entries:
                    current_entry = hass.config_entries.async_get_entry(entry_id)
                    if current_entry and current_entry.domain == DOMAIN:
                        target_config_entry = current_entry
                        break

                if target_config_entry:
                    # 3. call the service function
                    processed_entries[target_config_entry.entry_id] = await async_handle_reload_data(
                        hass, target_config_entry, call
                    )

        if not processed_entries:
            return None

        # Return a single response if only one entry was reloaded, otherwise return all
        if len(processed_entries) == 1:
            return list(processed_entries.values())[0]

        return processed_entries

    # Register services (only once at component level)
    if not hass.services.has_service(DOMAIN, SERVICE_EXAMPLE_ACTION):
        hass.services.async_register(
            DOMAIN,
            SERVICE_EXAMPLE_ACTION,
            handle_example_action,
        )

    if not hass.services.has_service(DOMAIN, SERVICE_RELOAD_DATA):
        hass.services.async_register(
            DOMAIN,
            SERVICE_RELOAD_DATA,
            handle_reload_data,
            supports_response=SupportsResponse.OPTIONAL,
        )

    LOGGER.debug("Services registered for %s", DOMAIN)
