"""Tests for converting IPX800 API data for entities."""

import pytest

from custom_components.my_ipx800v3.coordinator.data_processing import transform_api_data


@pytest.mark.unit
def test_analog_input_uses_its_configured_conversion() -> None:
    """Analog voltage inputs are converted to volts."""
    data = transform_api_data(
        {
            "analog0": "100",
            "anselect0": "1",
            "btn0": "dn",
            "led0": "0",
        }
    )

    assert data["analog0"] == pytest.approx(0.323)


@pytest.mark.unit
def test_invalid_api_data_is_returned_without_conversion() -> None:
    """Payloads missing required IPX800 keys are left unchanged."""
    data = {"analog0": "100"}

    assert transform_api_data(data) == data
