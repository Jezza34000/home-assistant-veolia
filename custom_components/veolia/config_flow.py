"""Adds config flow for Veolia."""

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from veolia_api import VeoliaAPI
from veolia_api.exceptions import VeoliaAPIError

from .const import DOMAIN


class VeoliaFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for veolia."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self) -> None:
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None) -> dict:
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            valid = await self._test_credentials(
                user_input[CONF_USERNAME],
                user_input[CONF_PASSWORD],
            )
            if valid:
                return self.async_create_entry(
                    title=user_input[CONF_USERNAME],
                    data=user_input,
                )
            self._errors["base"] = "auth"

            return await self._show_config_form(user_input)
        return await self._show_config_form(user_input)

    async def _show_config_form(self, user_input) -> dict:
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required(CONF_USERNAME): str, vol.Required(CONF_PASSWORD): str},
            ),
            errors=self._errors,
        )

    @staticmethod
    async def _test_credentials(username: str, password: str) -> bool:
        """Return true if credentials is valid."""
        try:
            api = VeoliaAPI(username, password)
            return await api.login()
        except VeoliaAPIError:
            pass
        return False
