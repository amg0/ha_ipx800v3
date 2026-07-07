"""Connectivity binary sensor for my_ipx800v3."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.my_ipx800v3.entity import MyIPX800V3Entity
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.const import EntityCategory

if TYPE_CHECKING:
    from custom_components.my_ipx800v3.coordinator import MyIPX800V3DataUpdateCoordinator

CONNECTIVITY_DESCRIPTION = BinarySensorEntityDescription(
    key="api_connectivity",
    translation_key="api_connectivity",
    device_class=BinarySensorDeviceClass.CONNECTIVITY,
    entity_category=EntityCategory.DIAGNOSTIC,
    icon="mdi:api",
    has_entity_name=True,
)


class MyIPX800V3ConnectivitySensor(BinarySensorEntity, MyIPX800V3Entity):
    """Connectivity sensor for my_ipx800v3."""

    def __init__(
        self,
        coordinator: MyIPX800V3DataUpdateCoordinator,
        entity_description: BinarySensorEntityDescription,
        api_endpoint: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entity_description)
        self._api_endpoint = api_endpoint

    @property
    def is_on(self) -> bool:
        """Return true if the API connection is established."""
        # Connection is considered established if coordinator has valid data
        return self.coordinator.last_update_success

    @property
    def extra_state_attributes(self) -> dict[str, str | None]:
        """Return additional state attributes."""
        return {
            "update_interval": str(self.coordinator.update_interval),
            "api_endpoint": self._api_endpoint,
            "ipx_key": "api_connectivity",
        }
