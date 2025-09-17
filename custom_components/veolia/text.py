"""Text entities for Veolia integration."""

from dataclasses import asdict

from homeassistant.components.text import TextEntity

from .const import DOMAIN, LOGGER, NAME


async def async_setup_entry(hass, entry, async_add_entities) -> None:
    """Set up text platform."""
    LOGGER.debug("Setting up text platform")
    coordinator = hass.data[DOMAIN][entry.entry_id]
    texts = [
        DailyThresholdText(coordinator, entry),
        MonthlyThresholdText(coordinator, entry),
    ]
    async_add_entities(texts)


class DailyThresholdText(TextEntity):
    """Representation of the daily threshold text entity."""

    def __init__(self, coordinator, config_entry) -> None:
        """Initialize the entity."""
        self.coordinator = coordinator
        self.config_entry = config_entry

    @property
    def device_info(self) -> dict:
        """Return device registry information for this entity."""
        return {
            "identifiers": {(DOMAIN, self.config_entry.entry_id)},
            "manufacturer": NAME,
            "name": f"{NAME} {self.coordinator.data.id_abonnement}",
        }

    @property
    def unique_id(self) -> str:
        """Return a unique ID to use for this entity."""
        return f"{self.config_entry.entry_id}_daily_threshold_text"

    @property
    def has_entity_name(self) -> bool:
        """Indicate that entity has name defined."""
        return True

    @property
    def translation_key(self) -> str:
        """Translation key for this entity."""
        return "daily_threshold_text"

    @property
    def native_max(self) -> int:
        """Max number of characters."""
        return 6

    @property
    def native_min(self) -> int:
        """Min number of characters."""
        return 1

    @property
    def pattern(self) -> str:
        """Check validity with regex pattern."""
        return "^(?:0|[1-9][0-9]{2,3}|10000)$"

    @property
    def icon(self) -> str:
        """Return the icon of the text entity."""
        return "mdi:water-alert"

    @property
    def available(self) -> bool:
        """Return true if the text entity is available."""
        return not (
            self.coordinator.data.alert_settings.daily_enabled
            and self.coordinator.data.alert_settings.daily_threshold == 0
        )

    @property
    def native_value(self) -> str:
        """Return the current threshold value."""
        return str(self.coordinator.data.alert_settings.daily_threshold or 0)

    async def async_set_value(self, value: str) -> None:
        """Set the threshold value."""
        if int(value) == 0:
            self.coordinator.data.alert_settings.daily_enabled = False
        else:
            self.coordinator.data.alert_settings.daily_enabled = True
            self.coordinator.data.alert_settings.daily_threshold = value
            self.coordinator.data.alert_settings.daily_notif_email = True
            self.coordinator.data.alert_settings.daily_notif_sms = False

        LOGGER.debug(
            "Setting daily threshold to %s",
            asdict(self.coordinator.data.alert_settings),
        )
        res = await self.coordinator.client_api.set_alerts_settings(
            self.coordinator.data.alert_settings
        )
        if not res:
            message = f"Failed to set alert= {self.__class__.__qualname__} settings= {asdict(self.coordinator.data.alert_settings)}"
            raise RuntimeError(message)
        await self.coordinator.async_request_refresh()
        self.async_write_ha_state()


class MonthlyThresholdText(TextEntity):
    """Representation of the monthly threshold text entity."""

    def __init__(self, coordinator, config_entry) -> None:
        """Initialize the entity."""
        self.coordinator = coordinator
        self.config_entry = config_entry

    @property
    def device_info(self) -> dict:
        """Return device registry information for this entity."""
        return {
            "identifiers": {(DOMAIN, self.config_entry.entry_id)},
            "manufacturer": NAME,
            "name": f"{NAME} {self.coordinator.data.id_abonnement}",
        }

    @property
    def unique_id(self) -> str:
        """Return a unique ID to use for this entity."""
        return f"{self.config_entry.entry_id}_monthly_threshold_text"

    @property
    def has_entity_name(self) -> bool:
        """Indicate that entity has name defined."""
        return True

    @property
    def translation_key(self) -> str:
        """Translation key for this entity."""
        return "monthly_threshold_text"

    @property
    def native_max(self) -> int:
        """Max number of characters."""
        return 4

    @property
    def native_min(self) -> int:
        """Min number of characters."""
        return 1

    @property
    def pattern(self) -> str:
        """Check validity with regex pattern."""
        return "^(?:0|[1-9][0-9]{0,2}|1000)$"

    @property
    def icon(self) -> str:
        """Return the icon of the text entity."""
        return "mdi:water-alert"

    @property
    def available(self) -> bool:
        """Return true if the text entity is available."""
        return not (
            self.coordinator.data.alert_settings.daily_enabled
            and self.coordinator.data.alert_settings.daily_threshold == 0
        )

    @property
    def native_value(self) -> str:
        """Return the current threshold value."""
        return str(self.coordinator.data.alert_settings.monthly_threshold or 0)

    async def async_set_value(self, value: str) -> None:
        """Set the threshold value."""
        if int(value) == 0:
            self.coordinator.data.alert_settings.monthly_enabled = False
        else:
            self.coordinator.data.alert_settings.monthly_enabled = True
            self.coordinator.data.alert_settings.monthly_threshold = value
            self.coordinator.data.alert_settings.monthly_notif_email = True
            self.coordinator.data.alert_settings.monthly_notif_sms = False

        LOGGER.debug(
            "Setting monthly threshold to %s",
            asdict(self.coordinator.data.alert_settings),
        )
        res = await self.coordinator.client_api.set_alerts_settings(
            self.coordinator.data.alert_settings
        )
        if not res:
            message = f"Failed to set alert= {self.__class__.__qualname__} settings= {asdict(self.coordinator.data.alert_settings)}"
            raise RuntimeError(message)
        await self.coordinator.async_request_refresh()
        self.async_write_ha_state()
