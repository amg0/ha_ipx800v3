"""Config flow discovery shim — hassfest requires this module at the integration root."""

from .config_flow_handler import MyIPX800V3ConfigFlowHandler

__all__ = ["MyIPX800V3ConfigFlowHandler"]
