"""
Credential validators.

Validation functions for user credentials and authentication.

When this file grows, consider splitting into:
- credentials.py: Basic credential validation
- oauth.py: OAuth-specific validation
- api_auth.py: API authentication methods
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.my_ipx800v3.api import MyIPX800V3ApiClient
from homeassistant.helpers.aiohttp_client import async_create_clientsession

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant


async def validate_credentials(
    hass: HomeAssistant,
    host: str,
    port: int,
    username: str,
    password: str,
) -> dict[str, str]:
    """
    Validate user credentials by testing API connection.

    Args:
        hass: Home Assistant instance.
        host: The host/IP address of the IPX800 V3.
        port: The HTTP port of the IPX800 V3.
        username: The optional username.
        password: The optional password.

    Raises:
        MyIPX800V3ApiClientAuthenticationError: If credentials are invalid.
        MyIPX800V3ApiClientCommunicationError: If communication fails.
        MyIPX800V3ApiClientError: For other API errors.

    """
    client = MyIPX800V3ApiClient(
        host=host,
        port=port,
        username=username,
        password=password,
        session=async_create_clientsession(hass),
    )
    return await client.async_get_data()  # May raise authentication/communication errors


__all__ = [
    "validate_credentials",
]
