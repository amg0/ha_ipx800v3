"""
API package for my_ipx800v3.

Exception hierarchy:
    MyIPX800V3ApiClientError (base)
    ├── MyIPX800V3ApiClientCommunicationError (network/timeout)
    │   └── MyIPX800V3ApiClientRateLimitError (429, carries retry_after)
    └── MyIPX800V3ApiClientAuthenticationError (401/403)

The coordinator maps them onto ConfigEntryAuthFailed and UpdateFailed; nothing else
in the integration imports this package.
"""

from .client import (
    FAN_SPEEDS,
    MyIPX800V3ApiClient,
    MyIPX800V3ApiClientAuthenticationError,
    MyIPX800V3ApiClientCommunicationError,
    MyIPX800V3ApiClientError,
    MyIPX800V3ApiClientRateLimitError,
)

__all__ = [
    "FAN_SPEEDS",
    "MyIPX800V3ApiClient",
    "MyIPX800V3ApiClientAuthenticationError",
    "MyIPX800V3ApiClientCommunicationError",
    "MyIPX800V3ApiClientError",
    "MyIPX800V3ApiClientRateLimitError",
]
