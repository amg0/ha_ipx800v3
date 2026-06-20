"""
Config flow for my_ipx800v3.

This module implements the main configuration flow including:
- Initial user setup
- Reconfiguration of existing entries
- Reauthentication flow

For more information:
https://developers.home-assistant.io/docs/config_entries_config_flow_handler
"""

from __future__ import annotations

from typing import Any

from slugify import slugify

from custom_components.my_ipx800v3.config_flow_handler.options_flow import MyIPX800V3OptionsFlow
from custom_components.my_ipx800v3.config_flow_handler.schemas import (
    get_options_schema,
    get_reconfigure_schema,
    get_user_schema,
)
from custom_components.my_ipx800v3.config_flow_handler.validators import validate_credentials
from custom_components.my_ipx800v3.const import CONF_WEBHOOK_ID, CONF_WEBHOOK_URL, DOMAIN, LOGGER
from homeassistant import config_entries
from homeassistant.components import webhook
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_PORT, CONF_USERNAME
from homeassistant.loader import async_get_loaded_integration

# Map exception types to error keys for user-facing messages
ERROR_MAP = {
    "MyIPX800V3ApiClientAuthenticationError": "auth",
    "MyIPX800V3ApiClientCommunicationError": "connection",
}


class MyIPX800V3ConfigFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """
    Handle a config flow for my_ipx800v3.

    This class manages the configuration flow for the integration, including
    initial setup, reconfiguration, and reauthentication.

    Supported flows:
    - user: Initial setup via UI
    - reconfigure: Update existing configuration
    - reauth: Handle expired credentials

    For more details:
    https://developers.home-assistant.io/docs/config_entries_config_flow_handler
    """

    # Set by developer
    VERSION = 1
    MINOR_VERSION = 1

    ### MODIFICATION 2 : Initialisation d'un dictionnaire pour stocker temporairement les données du premier écran
    def __init__(self) -> None:
        """Initialize the ConfigFlow."""
        self._setup_data: dict[str, Any] = {}

    @staticmethod
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> MyIPX800V3OptionsFlow:
        """
        Get the options flow for this handler.

        Returns:
            The options flow instance for modifying integration options.
        """

        return MyIPX800V3OptionsFlow()

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """
        Handle a flow initialized by the user.

        This is the entry point when a user adds the integration from the UI.

        Args:
            user_input: The user input from the config flow form, or None for initial display.

        Returns:
            The config flow result, either showing a form or creating an entry.

        """
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                data = await validate_credentials(
                    self.hass,
                    host=user_input[CONF_HOST],
                    port=user_input[CONF_PORT],
                    username=user_input.get(CONF_USERNAME, ""),
                    password=user_input.get(CONF_PASSWORD, ""),
                )
            except Exception as exception:  # noqa: BLE001
                errors["base"] = self._map_exception_to_error(exception)
            else:
                # Set unique ID based on mac address from API data to prevent duplicates
                await self.async_set_unique_id(self._build_unique_id(data))
                self._abort_if_unique_id_configured()
                user_input[CONF_WEBHOOK_ID] = self.webhook_id
                user_input[CONF_WEBHOOK_URL] = self.webhook_url
                ### MODIFICATION 3 : Au lieu de créer l'entrée, on sauvegarde les données
                ### et on passe à la nouvelle étape `options_init`
                self._setup_data = user_input
                return await self.async_step_options_init()

        integration = async_get_loaded_integration(self.hass, DOMAIN)
        assert integration.documentation is not None, "Integration documentation URL is not set in manifest.json"
        self.webhook_id = webhook.async_generate_id()
        self.webhook_url = webhook.async_generate_url(self.hass, self.webhook_id)
        return self.async_show_form(
            step_id="user",
            data_schema=get_user_schema(user_input),
            errors=errors,
            description_placeholders={"documentation_url": integration.documentation, "webhook_url": self.webhook_url},
        )

    ### MODIFICATION 4 : Création de l'étape intermédiaire pour afficher le formulaire des options
    async def async_step_options_init(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle the options step during the initial setup."""
        if user_input is not None:
            host = self._setup_data[CONF_HOST]

            # C'est ici que l'entrée est réellement créée avec les 'data' ET les 'options'
            return self.async_create_entry(
                title=f"IPX800 V3 ({host})",
                data=self._setup_data,
                options=user_input,
            )

        # On récupère l'url du webhook précédemment générée pour le placeholder (comme dans votre options_flow.py)
        webhook_url = self._setup_data.get(CONF_WEBHOOK_URL, "")

        return self.async_show_form(
            step_id="options_init",
            data_schema=get_options_schema(),  # Pas de 'defaults' la première fois
            description_placeholders={"webhook_url": webhook_url},
        )

    async def async_step_reconfigure(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """
        Handle reconfiguration of the integration.

        Allows users to update the scan interval without removing and re-adding
        the integration.

        Args:
            user_input: The user input from the reconfigure form, or None for initial display.

        Returns:
            The config flow result, either showing a form or updating the entry.

        """
        entry = self._get_reconfigure_entry()
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                host = entry.data[CONF_HOST]
                port = entry.data[CONF_PORT]
                data = await validate_credentials(
                    self.hass,
                    host=host,
                    port=port,
                    username=user_input.get(CONF_USERNAME, ""),
                    password=user_input.get(CONF_PASSWORD, ""),
                )
            except Exception as exception:  # noqa: BLE001
                errors["base"] = self._map_exception_to_error(exception)
            else:
                uniqueid = self._build_unique_id(data)
                await self.async_set_unique_id(uniqueid)
                self._abort_if_unique_id_mismatch()
                return self.async_update_reload_and_abort(entry, data={**entry.data, **user_input})
                # return self.async_update_reload_and_abort(
                #     entry,
                #     data={**entry.data, **user_input},
                # )

        webhook_url = entry.data[CONF_WEBHOOK_URL]
        return self.async_show_form(
            step_id="reconfigure",
            data_schema=get_reconfigure_schema(entry.data),
            errors=errors,
            description_placeholders={"webhook_url": webhook_url},
        )

    def _build_unique_id(self, data):
        return slugify(f"{data['config_mac']}")

    # async def async_step_reauth(
    #     self,
    #     entry_data: dict[str, Any] | None = None,
    # ) -> config_entries.ConfigFlowResult:
    #     """
    #     Handle reauthentication when credentials are invalid.

    #     This flow is automatically triggered when the coordinator catches
    #     an authentication error (ConfigEntryAuthFailed).

    #     Args:
    #         entry_data: The existing entry data (unused, per convention).

    #     Returns:
    #         The result of the reauth_confirm step.

    #     """
    #     return await self.async_step_reauth_confirm()

    # async def async_step_reauth_confirm(
    #     self,
    #     user_input: dict[str, Any] | None = None,
    # ) -> config_entries.ConfigFlowResult:
    #     """
    #     Handle reauthentication confirmation.

    #     Shows the reauthentication form and processes updated credentials.

    #     Args:
    #         user_input: The user input with updated credentials, or None for initial display.

    #     Returns:
    #         The config flow result, either showing a form or updating the entry.

    #     """
    #     entry = self._get_reauth_entry()
    #     errors: dict[str, str] = {}

    #     if user_input is not None:
    #         try:
    #             await validate_credentials(
    #                 self.hass,
    #                 host=entry.data[CONF_HOST],
    #                 port=int(entry.data[CONF_PORT]),
    #                 username=user_input.get(CONF_USERNAME, ""),
    #                 password=user_input.get(CONF_PASSWORD, ""),
    #             )
    #         except Exception as exception:
    #             errors["base"] = self._map_exception_to_error(exception)
    #         else:
    #             return self.async_update_reload_and_abort(
    #                 entry,
    #                 data={**entry.data, **user_input},
    #             )

    #     return self.async_show_form(
    #         step_id="reauth_confirm",
    #         data_schema=get_reauth_schema(entry.data.get(CONF_USERNAME, "")),
    #         errors=errors,
    #         description_placeholders={
    #             "username": entry.data.get(CONF_USERNAME, ""),
    #         },
    #     )

    def _map_exception_to_error(self, exception: Exception) -> str:
        """
        Map API exceptions to user-facing error keys.

        Args:
            exception: The exception that was raised.

        Returns:
            The error key for display in the config flow form.

        """
        LOGGER.warning("Error in config flow: %s", exception)
        exception_name = type(exception).__name__
        return ERROR_MAP.get(exception_name, "unknown")


__all__ = ["MyIPX800V3ConfigFlowHandler"]
