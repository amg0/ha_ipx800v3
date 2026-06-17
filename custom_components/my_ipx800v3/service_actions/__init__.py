"""Service actions package for my_ipx800v3."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from custom_components.my_ipx800v3.const import DOMAIN, LOGGER
from custom_components.my_ipx800v3.service_actions.counter_service import (
    async_handle_change_counter_value,
    async_handle_set_counter_value,
)
from custom_components.my_ipx800v3.service_actions.example_service import (
    async_handle_reload_data,
    async_handle_toggle_input,
)
from homeassistant.core import ServiceCall, ServiceResponse, SupportsResponse
from homeassistant.helpers import device_registry as dr, entity_registry as er, target as target_helpers

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

# Service action names - only used within service_actions module
SERVICE_RELOAD_DATA = "reload_data"
SERVICE_TOGGLE_INPUT = "toggle_input"
SERVICE_SET_COUNTER_VALUE = "set_counter_value"
SERVICE_ADJUST_COUNTER_VALUE = "adjust_counter_value"


async def async_setup_services(hass: HomeAssistant) -> None:  # noqa: C901
    """Register services for the integration."""

    async def handle_toggle_input(call: ServiceCall) -> None:
        """Handle the toggle_input service call."""
        target_selection = target_helpers.TargetSelection(call.data)
        entity_registry = er.async_get(hass)

        for entity_id in target_selection.entity_ids:
            entity_entry = entity_registry.async_get(entity_id)
            if not entity_entry or not entity_entry.config_entry_id:
                continue

            target_config_entry = hass.config_entries.async_get_entry(entity_entry.config_entry_id)
            if not target_config_entry or target_config_entry.domain != DOMAIN:
                continue

            if not entity_entry.unique_id:
                continue

            unique_id_parts = entity_entry.unique_id.split("_", 1)
            if len(unique_id_parts) < 2:
                continue

            if not unique_id_parts[1].startswith(("btn", "led")) or not unique_id_parts[1][3:].isdigit():
                continue

            await async_handle_toggle_input(hass, target_config_entry, call, entity_key=unique_id_parts[1])

    async def handle_reload_data(call: ServiceCall) -> ServiceResponse:
        """Handle the reload_data service call."""
        target_selection = target_helpers.TargetSelection(call.data)
        device_registry = dr.async_get(hass)
        entity_registry = er.async_get(hass)

        device_ids = set(target_selection.device_ids)
        for entity_id in target_selection.entity_ids:
            if (entity_entry := entity_registry.async_get(entity_id)) and entity_entry.device_id:
                device_ids.add(entity_entry.device_id)

        processed_entries: dict[str, Any] = {}
        for device_id in device_ids:
            device_entry = device_registry.async_get(device_id)
            if not device_entry:
                continue

            if not any(
                (entry := hass.config_entries.async_get_entry(entry_id)) and entry.domain == DOMAIN
                for entry_id in device_entry.config_entries
            ):
                continue

            for entry_id in device_entry.config_entries:
                target_config_entry = hass.config_entries.async_get_entry(entry_id)
                if target_config_entry and target_config_entry.domain == DOMAIN:
                    processed_entries[target_config_entry.entry_id] = await async_handle_reload_data(
                        hass, target_config_entry, call
                    )

        if not processed_entries:
            return {}

        if len(processed_entries) == 1:
            return list(processed_entries.values())[0]

        return processed_entries

    async def handle_counter_action(call: ServiceCall) -> None:
        """Handle counter service calls."""
        target_selection = target_helpers.TargetSelection(call.data)
        entity_registry = er.async_get(hass)

        for entity_id in target_selection.entity_ids:
            entity_entry = entity_registry.async_get(entity_id)
            if not entity_entry or not entity_entry.config_entry_id:
                continue

            target_config_entry = hass.config_entries.async_get_entry(entity_entry.config_entry_id)
            if not target_config_entry or target_config_entry.domain != DOMAIN:
                continue

            if not entity_entry.unique_id:
                continue

            unique_id_parts = entity_entry.unique_id.split("_", 1)
            if len(unique_id_parts) < 2:
                continue

            entity_key = unique_id_parts[1]
            if not entity_key.startswith("count") or not entity_key[5:].isdigit():
                LOGGER.warning(
                    "Service %s only supports counter entities, but was called on %s",
                    call.service,
                    entity_id,
                )
                continue

            if call.service == SERVICE_SET_COUNTER_VALUE:
                await async_handle_set_counter_value(hass, target_config_entry, call, entity_key)
            elif call.service == SERVICE_ADJUST_COUNTER_VALUE:
                await async_handle_change_counter_value(hass, target_config_entry, call, entity_key)

    services = [
        (SERVICE_RELOAD_DATA, handle_reload_data, SupportsResponse.OPTIONAL),
        (SERVICE_TOGGLE_INPUT, handle_toggle_input, SupportsResponse.NONE),
        (SERVICE_SET_COUNTER_VALUE, handle_counter_action, SupportsResponse.NONE),
        (SERVICE_ADJUST_COUNTER_VALUE, handle_counter_action, SupportsResponse.NONE),
    ]

    for name, handler, supports_response in services:
        if not hass.services.has_service(DOMAIN, name):
            hass.services.async_register(
                DOMAIN,
                name,
                handler,
                supports_response=supports_response,
            )

    LOGGER.debug("Services registered for %s", DOMAIN)
