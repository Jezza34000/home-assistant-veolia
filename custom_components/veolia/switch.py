"""Switch platform for Veolia."""

from dataclasses import asdict

from homeassistant.components.switch import SwitchEntity

from .const import DOMAIN, LOGGER, NAME


async def async_setup_entry(hass, entry, async_add_devices) -> None:
    """Set up switch platform."""
    LOGGER.debug("Setting up switch platform")
    coordinator = hass.data[DOMAIN][entry.entry_id]
    switches = [
        DailySMSAlerts(coordinator, entry),
        MonthlySMSAlerts(coordinator, entry),
        UnoccupiedAlertSwitch(coordinator, entry),
    ]
    async_add_devices(switches)


class DailySMSAlerts(SwitchEntity):
    """Representation of the daily SMS alert switch."""

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
            "name": NAME,
        }

    @property
    def unique_id(self) -> str:
        """Return a unique ID to use for this entity."""
        return f"{self.config_entry.entry_id}_daily_sms_alert_switch"

    @property
    def has_entity_name(self) -> bool:
        """Indicate that entity has name defined."""
        return True

    @property
    def translation_key(self) -> str:
        """Translation key for this entity."""
        return "daily_sms_alert_switch"

    @property
    def icon(self) -> str:
        """Return the icon of the switch."""
        if bool(self.coordinator.data.alert_settings.daily_notif_sms):
            return "mdi:comment-check"
        return "mdi:comment-off"

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        return bool(self.coordinator.data.alert_settings.daily_notif_sms)

    @property
    def available(self) -> bool:
        """Return true if the switch is available."""
        return (
            not (
                self.coordinator.data.alert_settings.daily_enabled
                and self.coordinator.data.alert_settings.daily_threshold == 0
            )
            and self.coordinator.data.alert_settings.daily_enabled
        )

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the switch on."""
        LOGGER.debug("Turning on %s", self.__class__.__qualname__)
        self.coordinator.data.alert_settings.daily_notif_sms = True
        res = await self.coordinator.client_api.set_alerts_settings(
            self.coordinator.data.alert_settings
        )
        if not res:
            message = f"Failed to set alert= {self.__class__.__qualname__} settings= {asdict(self.coordinator.data.alert_settings)}"
            raise RuntimeError(message)
        await self.coordinator.async_request_refresh()
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the switch off."""
        LOGGER.debug("Turning off %s", self.__class__.__qualname__)
        self.coordinator.data.alert_settings.daily_notif_sms = False
        res = await self.coordinator.client_api.set_alerts_settings(
            self.coordinator.data.alert_settings
        )
        if not res:
            message = f"Failed to set alert= {self.__class__.__qualname__} settings= {asdict(self.coordinator.data.alert_settings)}"
            raise RuntimeError(message)
        await self.coordinator.async_request_refresh()
        self.async_write_ha_state()


class MonthlySMSAlerts(SwitchEntity):
    """Representation of the monthly SMS alert switch."""

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
        return f"{self.config_entry.entry_id}_monthly_sms_alert_switch"

    @property
    def has_entity_name(self) -> bool:
        """Indicate that entity has name defined."""
        return True

    @property
    def translation_key(self) -> str:
        """Translation key for this entity."""
        return "monthly_sms_alert_switch"

    @property
    def icon(self) -> str:
        """Return the icon of the switch."""
        if bool(self.coordinator.data.alert_settings.monthly_notif_sms):
            return "mdi:comment-check"
        return "mdi:comment-off"

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        return bool(self.coordinator.data.alert_settings.monthly_notif_sms)

    @property
    def available(self) -> bool:
        """Return true if the switch is available."""
        return (
            not (
                self.coordinator.data.alert_settings.daily_enabled
                and self.coordinator.data.alert_settings.daily_threshold == 0
            )
            and self.coordinator.data.alert_settings.monthly_enabled
        )

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the switch on."""
        LOGGER.debug("Turning on %s", self.__class__.__qualname__)
        self.coordinator.data.alert_settings.monthly_notif_sms = True
        res = await self.coordinator.client_api.set_alerts_settings(
            self.coordinator.data.alert_settings
        )
        if not res:
            message = f"Failed to set alert= {self.__class__.__qualname__} settings= {asdict(self.coordinator.data.alert_settings)}"
            raise RuntimeError(message)
        await self.coordinator.async_request_refresh()
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the switch off."""
        LOGGER.debug("Turning off %s", self.__class__.__qualname__)
        self.coordinator.data.alert_settings.monthly_notif_sms = False
        res = await self.coordinator.client_api.set_alerts_settings(
            self.coordinator.data.alert_settings
        )
        if not res:
            message = f"Failed to set alert= {self.__class__.__qualname__} settings= {asdict(self.coordinator.data.alert_settings)}"
            raise RuntimeError(message)
        await self.coordinator.async_request_refresh()
        self.async_write_ha_state()


class UnoccupiedAlertSwitch(SwitchEntity):
    """Representation of the switch to activate the unoccupied alert."""

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
        return f"{self.config_entry.entry_id}_unoccupied_alert_switch"

    @property
    def has_entity_name(self) -> bool:
        """Indicate that entity has name defined."""
        return True

    @property
    def translation_key(self) -> str:
        """Translation key for this entity."""
        return "unoccupied_alert_switch"

    @property
    def icon(self) -> str:
        """Return the icon of the switch."""
        if (
            bool(self.coordinator.data.alert_settings.daily_enabled)
            and self.coordinator.data.alert_settings.daily_threshold == 0
        ):
            return "mdi:comment-check"
        return "mdi:comment-off"

    @property
    def is_on(self) -> bool:
        """Return true if the switch is on."""
        return (
            self.coordinator.data.alert_settings.daily_enabled
            and self.coordinator.data.alert_settings.daily_threshold == 0
        )

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the switch on."""
        LOGGER.debug("Turning on %s", self.__class__.__qualname__)
        self.coordinator.data.alert_settings.daily_enabled = True
        self.coordinator.data.alert_settings.daily_threshold = 0
        self.coordinator.data.alert_settings.daily_notif_sms = True
        self.coordinator.data.alert_settings.daily_notif_email = True
        res = await self.coordinator.client_api.set_alerts_settings(
            self.coordinator.data.alert_settings
        )
        if not res:
            message = f"Failed to set alert= {self.__class__.__qualname__} settings= {asdict(self.coordinator.data.alert_settings)}"
            raise RuntimeError(message)
        await self.coordinator.async_request_refresh()
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the switch off."""
        LOGGER.debug("Turning off %s", self.__class__.__qualname__)
        self.coordinator.data.alert_settings.daily_enabled = False
        res = await self.coordinator.client_api.set_alerts_settings(
            self.coordinator.data.alert_settings
        )
        if not res:
            message = f"Failed to set alert= {self.__class__.__qualname__} settings= {asdict(self.coordinator.data.alert_settings)}"
            raise RuntimeError(message)
        await self.coordinator.async_request_refresh()
        self.async_write_ha_state()
