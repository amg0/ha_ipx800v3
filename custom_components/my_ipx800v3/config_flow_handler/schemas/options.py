"""
Options flow schemas.

Schemas for the options flow that allows users to modify settings
after initial configuration.

When adding many options, consider grouping them:
- basic_options.py: Common settings (update interval, debug mode)
- advanced_options.py: Advanced settings
- device_options.py: Device-specific settings
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import voluptuous as vol

from custom_components.my_ipx800v3.const import DEFAULT_SCAN_INTERVAL
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.helpers import selector


def get_options_schema(defaults: Mapping[str, Any] | None = None) -> vol.Schema:
    """
    Get schema for options flow.

    Args:
        defaults: Optional dictionary of current option values.

    Returns:
        Voluptuous schema for options configuration.

    """
    defaults = defaults or {}
    return vol.Schema(
        {
            vol.Required(
                CONF_SCAN_INTERVAL,
                default=defaults.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
            ): vol.All(
                vol.Coerce(int),
                selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=1,
                        max=300,
                        step=1,
                        unit_of_measurement="s",
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
            ),
        },
    )


__all__ = [
    "get_options_schema",
]
