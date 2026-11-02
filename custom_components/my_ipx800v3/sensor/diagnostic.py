"""Diagnostic sensor descriptions for my_ipx800v3."""

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import EntityCategory, UnitOfRatio, UnitOfTime

from .entity import MyIPX800V3SensorEntityDescription

ENTITY_DESCRIPTIONS: tuple[MyIPX800V3SensorEntityDescription, ...] = (
    MyIPX800V3SensorEntityDescription(
        key="filter_life",
        translation_key="filter_life",
        entity_category=EntityCategory.DIAGNOSTIC,
        native_unit_of_measurement=UnitOfRatio.PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        value_fn=lambda data: data.get("filter_life"),
    ),
    MyIPX800V3SensorEntityDescription(
        key="runtime",
        translation_key="runtime",
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.HOURS,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=0,
        value_fn=lambda data: data.get("runtime"),
    ),
)
