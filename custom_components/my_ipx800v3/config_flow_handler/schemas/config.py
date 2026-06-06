"""
Config flow schemas.

Schemas for the main configuration flow steps:
- User setup
- Reconfiguration
- Reauthentication

When this file grows too large (>300 lines), consider splitting into:
- user.py: User setup schemas
- reauth.py: Reauthentication schemas
- reconfigure.py: Reconfiguration schemas
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import voluptuous as vol

from custom_components.my_ipx800v3.const import CONF_NAME_FROM_IPX
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_PORT, CONF_USERNAME
from homeassistant.helpers import selector


def get_user_schema(defaults: Mapping[str, Any] | None = None) -> vol.Schema:
    """
    Get schema for user step (initial setup).

    Args:
        defaults: Optional dictionary of default values to pre-populate the form.

    Returns:
        Voluptuous schema for user credentials input.

    """
    defaults = defaults or {}
    return vol.Schema(
        {
            vol.Required(
                CONF_HOST,
                default=defaults.get(CONF_HOST, vol.UNDEFINED),
            ): selector.TextSelector(
                selector.TextSelectorConfig(
                    type=selector.TextSelectorType.TEXT,
                ),
            ),
            vol.Required(
                CONF_PORT,
                default=defaults.get(CONF_PORT, 80),
            ): vol.All(
                selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=1,
                        max=65535,
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Coerce(int),
            ),
            vol.Optional(
                CONF_NAME_FROM_IPX,
                default=defaults.get(CONF_NAME_FROM_IPX, True),
            ): selector.BooleanSelector(),
            vol.Optional(
                CONF_USERNAME,
                default=defaults.get(CONF_USERNAME, ""),
            ): selector.TextSelector(
                selector.TextSelectorConfig(
                    type=selector.TextSelectorType.TEXT,
                ),
            ),
            vol.Optional(
                CONF_PASSWORD,
                default=defaults.get(CONF_PASSWORD, ""),
            ): selector.TextSelector(
                selector.TextSelectorConfig(
                    type=selector.TextSelectorType.PASSWORD,
                ),
            ),
        },
    )


def get_reconfigure_schema(defaults: Mapping[str, Any] | None = None) -> vol.Schema:
    """
    Get schema for reconfigure step.

    Args:
        username: Current username to pre-fill in the form.

    Returns:
        Voluptuous schema for reconfiguration.

    """
    defaults = defaults or {}
    return vol.Schema(
        {
            vol.Optional(
                CONF_NAME_FROM_IPX,
                default=defaults.get(CONF_NAME_FROM_IPX, True),
            ): selector.BooleanSelector(),
        },
    )


def get_reauth_schema(username: str) -> vol.Schema:
    """
    Get schema for reauthentication step.

    Args:
        username: Current username to pre-fill in the form.

    Returns:
        Voluptuous schema for reauthentication.

    """
    return vol.Schema(
        {
            vol.Optional(
                CONF_USERNAME,
                default=username,
            ): selector.TextSelector(
                selector.TextSelectorConfig(
                    type=selector.TextSelectorType.TEXT,
                ),
            ),
            vol.Optional(
                CONF_PASSWORD,
            ): selector.TextSelector(
                selector.TextSelectorConfig(
                    type=selector.TextSelectorType.PASSWORD,
                ),
            ),
        },
    )


__all__ = [
    "get_reauth_schema",
    "get_reconfigure_schema",
    "get_user_schema",
]
