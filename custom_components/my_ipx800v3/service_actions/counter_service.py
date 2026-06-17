"""Counter service action handlers for my_ipx800v3."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.my_ipx800v3.api.client import MyIPX800V3ApiClientError
from custom_components.my_ipx800v3.const import LOGGER
from homeassistant.exceptions import ServiceValidationError

if TYPE_CHECKING:
    from custom_components.my_ipx800v3.data import MyIPX800V3ConfigEntry
    from homeassistant.core import HomeAssistant, ServiceCall


async def async_handle_set_counter_value(
    hass: HomeAssistant,
    entry: MyIPX800V3ConfigEntry,
    call: ServiceCall,
    entity_key: str,
) -> None:
    """
    Handle the set_counter_value service action call.

    Args:
        hass: Home Assistant instance
        entry: Config entry for the integration
        call: Service call data
        entity_key: The entity key (e.g., 'count0')
    """
    client = entry.runtime_data.client
    value = call.data.get("value")

    if value is None:
        raise ServiceValidationError("No value provided in set_counter_value service call")

    # Extract counter index from entity key (e.g., 'count0' -> 0)
    try:
        counter_index = int(entity_key[5:])
    except (ValueError, IndexError) as err:
        msg = f"Invalid counter entity key: {entity_key}"
        raise ServiceValidationError(msg) from err

    try:
        await client.async_set_counter(counter_index, int(value))
        LOGGER.debug(
            "Successfully set counter %d to %d",
            counter_index,
            value,
        )
    except MyIPX800V3ApiClientError as err:
        LOGGER.error("Error setting counter value: %s", err)
        raise ServiceValidationError(f"Error setting counter value: {err}") from err


async def async_handle_change_counter_value(
    hass: HomeAssistant,
    entry: MyIPX800V3ConfigEntry,
    call: ServiceCall,
    entity_key: str,
) -> None:
    """
    Handle the adjust_counter_value service action call.

    Args:
        hass: Home Assistant instance
        entry: Config entry for the integration
        call: Service call data
        entity_key: The entity key (e.g., 'count0')
    """
    client = entry.runtime_data.client
    offset = call.data.get("offset")

    if offset is None:
        raise ServiceValidationError("No offset provided in adjust_counter_value service call")

    offset = int(offset)
    if offset == 0:
        return

    # Extract counter index from entity key
    try:
        counter_index = int(entity_key[5:])
    except (ValueError, IndexError) as err:
        msg = f"Invalid counter entity key: {entity_key}"
        raise ServiceValidationError(msg) from err

    try:
        if offset > 0:
            await client.async_increment_counter(counter_index, offset)
        else:
            await client.async_decrement_counter(counter_index, abs(offset))

        LOGGER.debug(
            "Successfully adjusted counter %d by %d",
            counter_index,
            offset,
        )
    except MyIPX800V3ApiClientError as err:
        LOGGER.error("Error adjusting counter value: %s", err)
        raise ServiceValidationError(f"Error adjusting counter value: {err}") from err
