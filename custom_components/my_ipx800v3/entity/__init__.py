"""
Entity package for my_ipx800v3.

Architecture:
    All platform entities inherit from (PlatformEntity, MyIPX800V3Entity).
    MRO order matters — platform-specific class first, then the integration base.
    Entities read data from coordinator.data and NEVER call the API client directly.
    Unique IDs follow the pattern: {entry_id}_{description.key}

See entity/base.py for the MyIPX800V3Entity base class.
"""

from .base import MyIPX800V3Entity

__all__ = ["MyIPX800V3Entity"]
