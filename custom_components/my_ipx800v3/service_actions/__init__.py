"""Service actions package for my_ipx800v3."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from custom_components.my_ipx800v3.const import DOMAIN, LOGGER
from custom_components.my_ipx800v3.service_actions.example_service import (
    async_handle_example_action,
    async_handle_reload_data,
)
from homeassistant.core import ServiceCall, ServiceResponse, SupportsResponse
from homeassistant.helpers import (
    device_registry as dr,
    entity_registry as er,  # Add this import
    target as target_helpers,
)

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
        entity_registry = er.async_get(hass)

        # Collect all unique device IDs from both devices and entities
        device_ids = set(target_selection.device_ids)

        # Resolve entities to devices
        for entity_id in target_selection.entity_ids:
            if (entity_entry := entity_registry.async_get(entity_id)) and entity_entry.device_id:
                device_ids.add(entity_entry.device_id)

        processed_entries: dict[str, Any] = {}

        # 2. find the proper ConfigEntry for each device_id in the target selection
        # target_selection.device_ids now includes all devices, not just yours
        for device_id in device_ids:
            device_entry = device_registry.async_get(device_id)

            if not device_entry:
                continue

            # CRITICAL: Verify the device actually belongs to your integration
            # before attempting to process it.
            if not any(
                (entry := hass.config_entries.async_get_entry(entry_id)) and entry.domain == DOMAIN
                for entry_id in device_entry.config_entries
            ):
                continue  # Skip devices not belonging to my_ipx800v3

            # If we reach here, we know the device is ours.
            # Get the config entry properly to pass to your handler
            for entry_id in device_entry.config_entries:
                target_config_entry = hass.config_entries.async_get_entry(entry_id)
                if target_config_entry and target_config_entry.domain == DOMAIN:
                    # 3. call the service function
                    processed_entries[target_config_entry.entry_id] = await async_handle_reload_data(
                        hass, target_config_entry, call
                    )

        if not processed_entries:
            return {}

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
