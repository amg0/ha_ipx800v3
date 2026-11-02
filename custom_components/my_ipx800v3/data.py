"""
Runtime data types for my_ipx800v3.

Access pattern: entry.runtime_data.client / entry.runtime_data.coordinator
"""

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
    """Runtime data stored on the config entry after a successful setup."""

    client: MyIPX800V3ApiClient
    coordinator: MyIPX800V3DataUpdateCoordinator
    integration: Integration
