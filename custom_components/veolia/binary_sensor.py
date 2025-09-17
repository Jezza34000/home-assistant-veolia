"""The Veolia binary sensor integration."""

from homeassistant.components.binary_sensor import BinarySensorEntity

from .const import DOMAIN, LOGGER, NAME


async def async_setup_entry(hass, entry, async_add_devices) -> None:
    """Set up switch platform."""
    LOGGER.debug("Setting up binary_sensor platform")
    coordinator = hass.data[DOMAIN][entry.entry_id]
    switches = [
        DailyAlerts(coordinator, entry),
        MonthlyAlerts(coordinator, entry),
        UnoccupiedAlert(coordinator, entry),
    ]
    async_add_devices(switches)


class DailyAlerts(BinarySensorEntity):
    """Representation of the first alert binary sensor."""

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
            "name": f"{NAME} - {self.coordinator.data.id_abonnement}",
        }

    @property
    def unique_id(self) -> str:
        """Return a unique ID to use for this entity."""
        return f"{self.config_entry.entry_id}_daily_alert_binary_sensor"

    @property
    def has_entity_name(self) -> bool:
        """Indicate that entity has name defined."""
        return True

    @property
    def translation_key(self) -> str:
        """Translation key for this entity."""
        return "daily_alert_binary_sensor"

    @property
    def icon(self) -> str:
        """Return the icon of the binary sensor."""
        if bool(self.coordinator.data.alert_settings.daily_enabled):
            return "mdi:bell-check"
        return "mdi:bell-cancel"

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        return self.coordinator.data.alert_settings.daily_enabled

    @property
    def available(self) -> bool:
        """Return true if the binary sensor is available."""
        return not (
            self.coordinator.data.alert_settings.daily_enabled
            and self.coordinator.data.alert_settings.daily_threshold == 0
        )


class MonthlyAlerts(BinarySensorEntity):
    """Representation of the second alert binary sensor."""

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
            "name": f"{NAME} - {self.coordinator.data.id_abonnement}",
        }

    @property
    def unique_id(self) -> str:
        """Return a unique ID to use for this entity."""
        return f"{self.config_entry.entry_id}_monthly_alert_binary_sensor"

    @property
    def has_entity_name(self) -> bool:
        """Indicate that entity has name defined."""
        return True

    @property
    def translation_key(self) -> str:
        """Translation key for this entity."""
        return "monthly_alert_binary_sensor"

    @property
    def icon(self) -> str:
        """Return the icon of the binary sensor."""
        if bool(self.coordinator.data.alert_settings.monthly_enabled):
            return "mdi:bell-check"
        return "mdi:bell-cancel"

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        return bool(self.coordinator.data.alert_settings.monthly_enabled)

    @property
    def available(self) -> bool:
        """Return true if the binary sensor is available."""
        return not (
            self.coordinator.data.alert_settings.daily_enabled
            and self.coordinator.data.alert_settings.daily_threshold == 0
        )


class UnoccupiedAlert(BinarySensorEntity):
    """Representation of the unoccupied alert binary sensor."""

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
            "name": f"{NAME} - {self.coordinator.data.id_abonnement}",
        }

    @property
    def unique_id(self) -> str:
        """Return a unique ID to use for this entity."""
        return f"{self.config_entry.entry_id}_unoccupied_alert_binary_sensor"

    @property
    def has_entity_name(self) -> bool:
        """Indicate that entity has name defined."""
        return True

    @property
    def translation_key(self) -> str:
        """Translation key for this entity."""
        return "unoccupied_alert_binary_sensor"

    @property
    def icon(self) -> str:
        """Return the icon of the binary sensor."""
        if self.is_on:
            return "mdi:bell-check"
        return "mdi:bell-cancel"

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        return (
            self.coordinator.data.alert_settings.daily_enabled
            and self.coordinator.data.alert_settings.daily_threshold == 0
        )
