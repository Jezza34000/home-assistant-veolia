"""DataUpdateCoordinator for integration_blueprint."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from veolia_api import VeoliaAPI
from veolia_api.exceptions import VeoliaAPIError

from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util

from .const import DOMAIN, LOGGER
from .data import VeoliaConfigEntry
from .model import VeoliaModel

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant


class VeoliaDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: VeoliaConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
    ) -> None:
        """Initialize."""
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(hours=12),
        )
        LOGGER.debug("Initializing client VeoliaAPI")

        self.client_api = VeoliaAPI(
            username=self.config_entry.data[CONF_USERNAME],
            password=self.config_entry.data[CONF_PASSWORD],
        )

    async def _async_update_data(self) -> VeoliaModel:
        """Fetch and Calculate data."""
        try:
            now = datetime.now()
            await self.client_api.fetch_all_data(now.year, now.month)
            account_data = self.client_api.account_data
            today = dt_util.now().date()
            return VeoliaModel.from_account_data(account_data, today=today)
        except VeoliaAPIError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
