"""DataUpdateCoordinator for integration_blueprint."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from veolia_api import VeoliaAPI
from veolia_api.exceptions import VeoliaAPIError
from veolia_api.model import VeoliaAccountData
from veolia_api.veolia_api import ConsumptionType

from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, LOGGER
from .data import VeoliaConfigEntry

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

    async def _async_update_data(self) -> VeoliaAccountData:
        """Update data via library."""
        try:
            now = datetime.now()
            LOGGER.debug(
                f"Fetching consumption data for {ConsumptionType.MONTHLY.value} "
                f"Year:{now.year} Month:{now.month}",
            )
            await self.client_api.fetch_all_data(now.year, now.month)
            LOGGER.debug("Data fetched successfully = %s", self.client_api.account_data)
        except VeoliaAPIError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        else:
            return self.client_api.account_data
