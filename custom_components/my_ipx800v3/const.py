"""Constants for my_ipx800v3."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "my_ipx800v3"
ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"

CONF_FILTER_REPLACEMENT_THRESHOLD = "filter_replacement_threshold"
DEFAULT_FILTER_REPLACEMENT_THRESHOLD = 10
