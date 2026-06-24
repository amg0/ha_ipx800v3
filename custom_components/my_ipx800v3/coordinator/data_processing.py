"""
Data processing utilities for the coordinator.

This module provides functions for processing, transforming, and validating
data received from the API before distributing it to entities.

Use cases:
- Data normalization and validation
- Caching strategies for expensive computations
- Data transformation for entity consumption
- Aggregation of multiple API responses
"""

from __future__ import annotations

from typing import Any

from custom_components.my_ipx800v3.const import LOGGER


def validate_api_response(data: Any) -> bool:
    """
    Validate the structure and content of API response data.

    Args:
        data: The raw data received from the API.

    Returns:
        True if the data is valid, False otherwise.

    Example:
        >>> data = {"userId": 1, "id": 1, "title": "Test"}
        >>> validate_api_response(data)
        True
    """
    if not isinstance(data, dict):
        LOGGER.warning("Invalid API response: expected dict, got %s", type(data).__name__)
        return False

    # Add validation logic based on your API structure
    if "analog0" not in data or "led0" not in data or "btn0" not in data:
        LOGGER.warning("Invalid API response: missing required keys 'analog0' or 'led0' or 'btn0'")
        return False
    return True


def transform_api_data(raw_data: Any) -> dict[str, Any]:
    """
    Transform raw API data into a standardized format for entities.

    This function can be used to:
    - Normalize field names
    - Convert units
    - Calculate derived values
    - Restructure nested data

    For analog*x* keys, transforms based on the corresponding anselect*x* value:
    - Searches for all analog*x* keys in the raw data
    - For each analog*x*, finds the corresponding anselect*x* key with same index
    - Applies transformation based on the anselect*x* value
    - Default case returns the analog*x* value unchanged

    Args:
        raw_data: The raw data from the API.

    Returns:
        A dictionary with transformed data ready for entity consumption.

    Example:
        >>> raw = {"temp_c": 25.5}
        >>> transform_api_data(raw)
        {"temperature": 25.5, "temperature_f": 77.9}
    """
    if not validate_api_response(raw_data):
        LOGGER.warning("Skipping transformation of invalid data")
        return raw_data if isinstance(raw_data, dict) else {}

    transformed_data = dict(raw_data)

    # Find and process all analogXX keys
    # <select name="sel" id="select" style="width:186px;">Select Input:
    #     <option value="0" id="s0">Analog</option>
    #     <option value="1" id="s1">Volt</option>
    #     <option value="2" id="s2">TC4012 Sensor</option>
    #     <option value="3" id="s3">SHT-X3:Light-LS100</option>
    #     <option value="4" id="s4">SHT-X3:Temp-TC5050</option>
    #     <option value="5" id="s5">SHT-X3:RH-SH100</option>
    #     <option value="6" id="s6">TC100 Sensor</option>
    #     <option value="7" id="s7">X400 CT10A</option>
    #     <option value="8" id="s8">X400 CT20A</option>
    #     <option value="9" id="s9">X400 CT50A</option>
    #     <option value="12" id="s12">X400 CT100A</option>
    #     <option value="10" id="s10">X200 pH Probe</option>
    #     <option value="11" id="s11">X200 ORP Probe</option>
    # </select>
    analog_keys = [key for key in transformed_data if key.startswith("analog")]
    for analog_key in analog_keys:
        # Extract the index from analogXX
        index = analog_key[6:]  # Remove "analog" prefix
        anselect_key = f"anselect{index}"

        if anselect_key in transformed_data:
            anselect_value = transformed_data[anselect_key]
            analog_value = transformed_data[analog_key]

            # Switch based on anselect value
            match anselect_value:
                case "1":
                    transformed_data[analog_key] = float(analog_value) * 0.00323
                case "2":
                    transformed_data[analog_key] = float(analog_value) * 0.323 - 50
                case "3":
                    transformed_data[analog_key] = float(analog_value) * 0.09775
                case "4":
                    transformed_data[analog_key] = (float(analog_value) * 0.00323 - 1.63) / 0.0326
                case "5":
                    # --TODO humidity sensor so needs add hTemp correction but we do not know
                    # -- hTemp so let's take 15C as an average
                    # -- GetAn	HCTemp	0	10	20	30	40		Delta
                    # -- 0		0	0	0	0	0
                    # -- 10		9,482268159	9,68054211	9,887284952	10,10305112	10,32844454		0,846176378
                    # -- 20		18,96453632	19,36108422	19,7745699	20,20610224	20,65688907		1,692352755
                    # -- 30		28,44680448	29,04162633	29,66185485	30,30915336	30,98533361		2,538529133
                    # -- 40		37,92907263	38,72216844	39,54913981	40,41220449	41,31377815		3,384705511
                    HCtemp = 15
                    v = float(analog_value) * 0.00323
                    v = (v / 3.3 - 0.1515) / 0.00636
                    transformed_data[analog_key] = v / (1.0546 - (0.00216 * HCtemp))
                case "6":
                    transformed_data[analog_key] = (float(analog_value) * 0.00323 - 0.25) / 0.028
                case "7":
                    transformed_data[analog_key] = float(analog_value) * 0.00323
                case "8":
                    transformed_data[analog_key] = float(analog_value) * 0.00646
                case "9":
                    transformed_data[analog_key] = float(analog_value) * 0.01615
                case "10":
                    transformed_data[analog_key] = float(analog_value) / 100
                case "11":
                    transformed_data[analog_key] = float(analog_value) - 2500
                case "12":
                    transformed_data[analog_key] = float(analog_value) * 0.0323
                case _:
                    # Default case: return analog value unchanged
                    transformed_data[analog_key] = float(analog_value)
        else:
            # If no corresponding anselect key, keep original value
            pass

    # Transform data as needed
    # This is a placeholder for future implementation
    return transformed_data


def cache_computed_values(data: dict[str, Any]) -> dict[str, Any]:
    """
    Add computed or cached values to the coordinator data.

    This is useful for expensive calculations that should only be done once
    per update cycle rather than in each entity.

    Args:
        data: The base data dictionary.

    Returns:
        The data dictionary with additional computed values.

    Example:
        >>> data = {"power": 1000, "runtime": 3600}
        >>> cache_computed_values(data)
        {"power": 1000, "runtime": 3600, "energy_kwh": 1.0}
    """
    # Add computed values as needed
    # This is a placeholder for future implementation
    return data
