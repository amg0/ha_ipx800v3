"""Constants for my_ipx800v3."""

from logging import Logger, getLogger
from typing import Final

LOGGER: Logger = getLogger(__package__)

DOMAIN = "my_ipx800v3"
ATTRIBUTION = "Data provided by https://wiki.gce-electronics.com/index.php?title=API_V3"

DEFAULT_SCAN_INTERVAL = 60
DEFAULT_ENABLE_DEBUGGING = False

CONF_WEBHOOK_ID = "webhook_id"
CONF_WEBHOOK_URL = "webhook_url"
CONF_NAME_FROM_IPX = "names_from_ipx"
CONF_AUTOMATIC_PUSH = "automatic_push"

URL_BASE: Final[str] = "/my_ipx800v3"
