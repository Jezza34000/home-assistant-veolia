"""Sensor platform for Veolia."""

from .const import (
    CONSO,
    CONSO_FIABILITY,
    DATA_DATE,
    DOMAIN,
    IDX,
    IDX_FIABILITY,
    LAST_DATA,
    LITRE,
    LOGGER,
)
from .entity import VeoliaMesurements


async def async_setup_entry(hass, entry, async_add_devices) -> None:
    """Set up sensor platform."""
    LOGGER.debug("Setting up sensor platform")
    coordinator = hass.data[DOMAIN][entry.entry_id]
    sensors = [
        LastIndexSensor(coordinator, entry),
        DailyConsumption(coordinator, entry),
        MonthlyConsumption(coordinator, entry),
    ]
    async_add_devices(sensors)


class LastIndexSensor(VeoliaMesurements):
    """Monitors the last index."""

    @property
    def unique_id(self) -> str:
        """Return a unique ID to use for this entity."""
        return f"{self.config_entry.entry_id}_last_index"

    @property
    def has_entity_name(self) -> bool:
        """Indicate that entity has name defined."""
        return True

    @property
    def translation_key(self) -> str:
        """Translation key for this entity."""
        return "veolia_index"

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        state = self.coordinator.data.daily_consumption[LAST_DATA][IDX][LITRE]
        LOGGER.debug("Index consumption: %s L", state)
        return state if state > 0 else None

    @property
    def icon(self) -> str | None:
        """Set icon."""
        return "mdi:counter"

    @property
    def extra_state_attributes(self) -> dict:
        """Return the base extra state attributes."""
        return {
            "data_type": self.coordinator.data.daily_consumption[LAST_DATA][
                IDX_FIABILITY
            ],
            "last_report": self.coordinator.data.daily_consumption[LAST_DATA][
                DATA_DATE
            ],
        }


class DailyConsumption(VeoliaMesurements):
    """Monitors the last index."""

    @property
    def unique_id(self) -> str:
        """Return a unique ID to use for this entity."""
        return f"{self.config_entry.entry_id}_daily_consumption"

    @property
    def has_entity_name(self) -> bool:
        """Indicate that entity has name defined."""
        return True

    @property
    def translation_key(self) -> str:
        """Translation key for this entity."""
        return "daily_consumption"

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        state = self.coordinator.data.daily_consumption[LAST_DATA][CONSO][LITRE]
        LOGGER.debug("Daily consumption: %s L", state)
        return state if state > 0 else None

    @property
    def icon(self) -> str | None:
        """Set icon."""
        return "mdi:water"

    @property
    def extra_state_attributes(self) -> dict:
        """Return the base extra state attributes."""
        return {
            "data_type": self.coordinator.data.daily_consumption[LAST_DATA][
                IDX_FIABILITY
            ],
            "last_report": self.coordinator.data.daily_consumption[LAST_DATA][
                DATA_DATE
            ],
        }


class MonthlyConsumption(VeoliaMesurements):
    """Monitors the last index."""

    @property
    def unique_id(self) -> str:
        """Return a unique ID to use for this entity."""
        return f"{self.config_entry.entry_id}_monthly_consumption"

    @property
    def has_entity_name(self) -> bool:
        """Indicate that entity has name defined."""
        return True

    @property
    def translation_key(self) -> str:
        """Translation key for this entity."""
        return "monthly_consumption"

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        state = self.coordinator.data.monthly_consumption[LAST_DATA][CONSO][LITRE]
        LOGGER.debug("Monthly consumption: %s L", state)
        return state if state > 0 else None

    @property
    def icon(self) -> str | None:
        """Set icon."""
        return "mdi:water"

    @property
    def extra_state_attributes(self) -> dict:
        """Return the base extra state attributes."""
        return {
            "data_type": self.coordinator.data.monthly_consumption[LAST_DATA][
                CONSO_FIABILITY
            ],
        }
