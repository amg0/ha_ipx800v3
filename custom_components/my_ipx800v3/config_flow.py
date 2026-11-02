"""
Config flow for my_ipx800v3.

This module provides backwards compatibility for hassfest.
The actual implementation is in the config_flow_handler package.
"""

from __future__ import annotations

from .config_flow_handler import MyIPX800V3ConfigFlowHandler

__all__ = ["MyIPX800V3ConfigFlowHandler"]
