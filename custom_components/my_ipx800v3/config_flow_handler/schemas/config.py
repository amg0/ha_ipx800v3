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

from collections.abc import Mapping
from typing import Any

import probatio

from custom_components.my_ipx800v3.const import CONF_AUTOMATIC_PUSH, CONF_NAME_FROM_IPX
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_PORT, CONF_USERNAME
from homeassistant.helpers import selector


def get_user_schema(defaults: Mapping[str, Any] | None = None) -> probatio.Schema:
    """
    Get schema for user step (initial setup).

    Args:
        defaults: Optional dictionary of default values to pre-populate the form.

    Returns:
        Probatio schema for user credentials input.

    """
    defaults = defaults or {}
    return probatio.Schema(
        {
            probatio.Required(
                CONF_HOST,
                default=defaults.get(CONF_HOST, probatio.UNDEFINED),
            ): selector.TextSelector(
                selector.TextSelectorConfig(
                    type=selector.TextSelectorType.TEXT,
                ),
            ),
            probatio.Required(
                CONF_PORT,
                default=defaults.get(CONF_PORT, 80),
            ): probatio.All(
                selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=1,
                        max=65535,
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                probatio.Coerce(int),
            ),
            probatio.Optional(
                CONF_NAME_FROM_IPX,
                default=defaults.get(CONF_NAME_FROM_IPX, True),
            ): selector.BooleanSelector(),
            probatio.Optional(
                CONF_AUTOMATIC_PUSH,
                default=defaults.get(CONF_AUTOMATIC_PUSH, True),
            ): selector.BooleanSelector(),
            probatio.Optional(
                CONF_USERNAME,
                default=defaults.get(CONF_USERNAME, ""),
            ): selector.TextSelector(
                selector.TextSelectorConfig(
                    type=selector.TextSelectorType.TEXT,
                ),
            ),
            probatio.Optional(
                CONF_PASSWORD,
                default=defaults.get(CONF_PASSWORD, ""),
            ): selector.TextSelector(
                selector.TextSelectorConfig(
                    type=selector.TextSelectorType.PASSWORD,
                ),
            ),
        },
    )


def get_reconfigure_schema(defaults: Mapping[str, Any] | None = None) -> probatio.Schema:
    """
    Get schema for reconfigure step.

    Args:
        username: Current username to pre-fill in the form.

    Returns:
        Probatio schema for reconfiguration.

    """
    defaults = defaults or {}
    return probatio.Schema(
        {
            probatio.Optional(
                CONF_NAME_FROM_IPX,
                default=defaults.get(CONF_NAME_FROM_IPX, True),
            ): selector.BooleanSelector(),
            probatio.Optional(
                CONF_AUTOMATIC_PUSH,
                default=defaults.get(CONF_AUTOMATIC_PUSH, True),
            ): selector.BooleanSelector(),
        },
    )


def get_reauth_schema(username: str) -> probatio.Schema:
    """
    Get schema for reauthentication step.

    Args:
        username: Current username to pre-fill in the form.

    Returns:
        Probatio schema for reauthentication.

    """
    return probatio.Schema(
        {
            probatio.Optional(
                CONF_USERNAME,
                default=username,
            ): selector.TextSelector(
                selector.TextSelectorConfig(
                    type=selector.TextSelectorType.TEXT,
                ),
            ),
            probatio.Optional(
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
