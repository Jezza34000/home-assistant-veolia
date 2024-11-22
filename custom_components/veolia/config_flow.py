"""Adds config flow for Veolia."""

from veolia_api import VeoliaAPI
from veolia_api.exceptions import VeoliaAPIInvalidCredentialsError
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME

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
            try:
                api = VeoliaAPI(user_input[CONF_USERNAME], user_input[CONF_PASSWORD])
                valid = await api.login()

                if valid:
                    return self.async_create_entry(
                        title=user_input[CONF_USERNAME],
                        data=user_input,
                    )
            except VeoliaAPIInvalidCredentialsError:
                self._errors["base"] = "invalid_credentials"
            except Exception:  # noqa: BLE001
                self._errors["base"] = "unknown"

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
