"""Constants for my_ipx800v3."""

import json
from logging import Logger, getLogger
from pathlib import Path
from typing import Final

LOGGER: Logger = getLogger(__package__)

# Integration metadata
DOMAIN = "my_ipx800v3"
ATTRIBUTION = "Data provided by https://wiki.gce-electronics.com/index.php?title=API_V3"

# Platform parallel updates - applied to all platforms
PARALLEL_UPDATES = 1

# Default configuration values
DEFAULT_SCAN_INTERVAL = 60
DEFAULT_ENABLE_DEBUGGING = False

CONF_WEBHOOK_ID = "webhook_id"
CONF_WEBHOOK_URL = "webhook_url"
CONF_NAME_FROM_IPX = "names_from_ipx"
CONF_AUTOMATIC_PUSH = "automatic_push"

# Read version from manifest.json
MANIFEST_PATH = Path(__file__).parent / "manifest.json"
with Path.open(MANIFEST_PATH, encoding="utf-8") as f:
    INTEGRATION_VERSION: Final[str] = json.load(f).get("version", "0.0.0")

# Base URL for frontend resources
URL_BASE: Final[str] = "/my_ipx800v3"

# List of JavaScript modules to register
JSMODULES: Final[list[dict[str, str]]] = [
    {
        "name": "My IPX800 Card",
        "filename": "ipx800v3-card.js",
        "version": INTEGRATION_VERSION,
    },
    # Add editor if needed
    # {
    #     "name": "Your Card Editor",
    #     "filename": "your-card-editor.js",
    #     "version": INTEGRATION_VERSION,
    # },
]
