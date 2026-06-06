"""
Custom types for my_ipx800v3.

This module defines the runtime data structure attached to each config entry.
Access pattern: entry.runtime_data.client / entry.runtime_data.coordinator

The MyIPX800V3ConfigEntry type alias is used throughout the integration
for type-safe access to the config entry's runtime data.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import MyIPX800V3ApiClient
    from .coordinator import MyIPX800V3DataUpdateCoordinator


type MyIPX800V3ConfigEntry = ConfigEntry[MyIPX800V3Data]


@dataclass
class MyIPX800V3Data:
    """Runtime data for my_ipx800v3 config entries.

    Stored as entry.runtime_data after successful setup.
    Provides typed access to the API client and coordinator instances.
    """

    client: MyIPX800V3ApiClient
    coordinator: MyIPX800V3DataUpdateCoordinator
    integration: Integration
