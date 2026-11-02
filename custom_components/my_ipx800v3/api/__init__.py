"""
API package for my_ipx800v3.

Architecture:
    Three-layer data flow: Entities → Coordinator → API Client.
    Only the coordinator should call the API client. Entities must never
    import or call the API client directly.

Exception hierarchy:
    MyIPX800V3ApiClientError (base)
    ├── MyIPX800V3ApiClientCommunicationError (network/timeout)
    └── MyIPX800V3ApiClientAuthenticationError (401/403)

Coordinator exception mapping:
    ApiClientAuthenticationError → ConfigEntryAuthFailed (triggers reauth)
    ApiClientCommunicationError → UpdateFailed (auto-retry)
    ApiClientError             → UpdateFailed (auto-retry)
"""

from .client import (
    MyIPX800V3ApiClient,
    MyIPX800V3ApiClientAuthenticationError,
    MyIPX800V3ApiClientCommunicationError,
    MyIPX800V3ApiClientError,
)

__all__ = [
    "MyIPX800V3ApiClient",
    "MyIPX800V3ApiClientAuthenticationError",
    "MyIPX800V3ApiClientCommunicationError",
    "MyIPX800V3ApiClientError",
]
