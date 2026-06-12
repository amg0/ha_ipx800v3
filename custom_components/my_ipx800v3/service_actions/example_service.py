"""Example service action handlers for my_ipx800v3."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.my_ipx800v3.api.client import (
    MyIPX800V3ApiClientAuthenticationError,
    MyIPX800V3ApiClientCommunicationError,
    MyIPX800V3ApiClientError,
)
from custom_components.my_ipx800v3.const import LOGGER
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady, ServiceValidationError
from homeassistant.helpers.update_coordinator import UpdateFailed
from homeassistant.util import dt as dt_util

if TYPE_CHECKING:
    from custom_components.my_ipx800v3.data import MyIPX800V3ConfigEntry
    from homeassistant.core import HomeAssistant, ServiceCall, ServiceResponse


async def async_handle_example_action(
    hass: HomeAssistant,
    entry: MyIPX800V3ConfigEntry,
    call: ServiceCall,
) -> None:
    """
    Handle the example_action service action call.

    This is a dummy service action that demonstrates how to implement custom service actions.

    Args:
        hass: Home Assistant instance
        entry: Config entry for the integration
        call: Service call data
    """
    LOGGER.info("Example action service called with data: %s", call.data)

    # Example: Access the coordinator
    # coordinator = entry.runtime_data.coordinator

    # Example: Access the API client
    # client = entry.runtime_data.client

    # Example: Do something with the service call data
    action_type = call.data.get("action_type", "default")
    target_value = call.data.get("target_value")

    LOGGER.debug(
        "Processing action type: %s with target value: %s",
        action_type,
        target_value,
    )

    # In a real implementation, you would:
    # - Validate the input
    # - Call API methods via client
    # - Update coordinator data if needed
    # - Handle errors appropriately

    # For now, this is just a dummy that logs the action
    LOGGER.info("Example action completed successfully")


async def async_handle_toggle_input(
    hass: HomeAssistant,
    entry: MyIPX800V3ConfigEntry,
    call: ServiceCall,
    entity_key: str | None = None,
) -> None:
    """
    Handle the toggle_input service action call.

    This service toggles the state of a specific digital input entity.

    Args:
        hass: Home Assistant instance
        entry: Config entry for the integration
        call: Service call data containing target entity ID
        entity_key: Optional entity key override
    """
    client = entry.runtime_data.client

    # Extract entity key from parameters or service call data
    if entity_key is None:
        LOGGER.error("No entity key provided in toggle_input service call")
        raise ServiceValidationError("No entity key provided in toggle_input service call")

    # Extract digital input index from entity attributes
    input_index = int(entity_key[3])

    # IPX800V3 API requires adding 100 to the input index
    if entity_key.startswith("btn"):
        relay_index = input_index + 100
    elif entity_key.startswith("led"):
        relay_index = input_index
    else:
        LOGGER.error("Invalid entity key format: %s", entity_key)
        raise ServiceValidationError(f"Invalid entity key format: {entity_key}")

    try:
        await client.async_set_relay_switch(relay_index)
        LOGGER.debug(
            "Successfully toggled digital input %d for entity %s",
            input_index,
            entity_key,
        )
    except MyIPX800V3ApiClientAuthenticationError as err:
        LOGGER.error("Authentication error toggling input: %s", err)
        raise ServiceValidationError(f"Authentication error toggling input: {err}") from err
    except MyIPX800V3ApiClientCommunicationError as err:
        LOGGER.error("Communication error toggling input: %s", err)
        raise ServiceValidationError(f"Communication error toggling input: {err}") from err
    except MyIPX800V3ApiClientError as err:
        LOGGER.error("Error toggling input: %s", err)
        raise ServiceValidationError(f"Error toggling input: {err}") from err


async def async_handle_reload_data(
    hass: HomeAssistant,
    entry: MyIPX800V3ConfigEntry,
    call: ServiceCall,
) -> ServiceResponse:
    """
    Handle the reload_data service call with response data.

    This service forces a refresh of the integration data and returns
    diagnostic information about the refresh operation.

    Args:
        hass: Home Assistant instance
        entry: Config entry for the integration
        call: Service call data

    Returns:
        ServiceResponse: Dictionary with refresh status, timestamp, and data summary
    """
    LOGGER.info("Reload data service called")

    # Access the coordinator and trigger a refresh
    coordinator = entry.runtime_data.coordinator
    start_time = dt_util.now()

    try:
        await coordinator.async_request_refresh()
    except (UpdateFailed, ConfigEntryAuthFailed, ConfigEntryNotReady) as exception:
        LOGGER.exception("Failed to reload data: %s", exception)
        # Return error response instead of raising
        raise ServiceValidationError(f"Failed to reload data: {exception}") from exception
    else:
        end_time = dt_util.now()
        duration_ms = (end_time - start_time).total_seconds() * 1000

        # Count records in coordinator data
        data_size = len(str(coordinator.data)) if coordinator.data else 0
        record_count = len(coordinator.data) if isinstance(coordinator.data, dict) else 0

        response_data: ServiceResponse = {
            "status": "success",
            "timestamp": end_time.isoformat(),
            "duration_ms": round(duration_ms, 2),
            "record_count": record_count,
            "data_size_bytes": data_size,
            "last_update_success": coordinator.last_update_success,
        }

        LOGGER.info(
            "Data reload completed successfully in %.2fms with %d records",
            duration_ms,
            record_count,
        )
        return response_data
