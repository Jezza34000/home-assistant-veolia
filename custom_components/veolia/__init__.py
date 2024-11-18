"""The Veolia integration."""

import logging
import homeassistant.helpers.config_validation as cv

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dev_reg
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .coordinator import VeoliaDataUpdateCoordinator
from .data import VeoliaConfigEntry, VeoliaData
from .sensor import LastIndexSensor

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.SWITCH,
]

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Veolia integration."""
    return True


async def async_setup_entry(hass, entry):
    """Set up Veolia from a config entry."""
    coordinator = VeoliaDataUpdateCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: VeoliaConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: VeoliaConfigEntry,
) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)


async def async_remove_config_entry_device(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    device_entry: dev_reg.DeviceEntry,
) -> bool:
    """Remove a config entry from a device."""
    return True
