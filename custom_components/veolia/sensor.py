"""Sensor platform for Veolia."""

from datetime import datetime

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.const import UnitOfVolume
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    CONSO,
    CONSO_FIABILITY,
    CUBIC_METER,
    DATA_DATE,
    DOMAIN,
    IDX,
    IDX_FIABILITY,
    LAST_DATA,
    LITRE,
    LOGGER,
    NAME,
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
        AnnualConsumption(coordinator, entry),
        LastDateSensor(coordinator, entry),
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
        state = self.coordinator.data.daily_consumption[LAST_DATA][IDX][CUBIC_METER]
        LOGGER.debug("Index consumption: %s L", state)
        return state if state > 0 else None

    @property
    def state_class(self) -> str:
        """Return the state_class of the sensor."""
        return SensorStateClass.TOTAL_INCREASING

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit_of_measurement of the sensor."""
        return UnitOfVolume.CUBIC_METERS

    @property
    def suggested_display_precision(self) -> int:
        """Return the suggested display precision."""
        return 3

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
    def state_class(self) -> str:
        """Return the state_class of the sensor."""
        return SensorStateClass.TOTAL

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit_of_measurement of the sensor."""
        return UnitOfVolume.LITERS

    @property
    def suggested_display_precision(self) -> int:
        """Return the suggested display precision."""
        return 0

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
    def state_class(self) -> str:
        """Return the state_class of the sensor."""
        return SensorStateClass.TOTAL_INCREASING

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit_of_measurement of the sensor."""
        return UnitOfVolume.LITERS

    @property
    def suggested_display_precision(self) -> int:
        """Return the suggested display precision."""
        return 0

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


class AnnualConsumption(VeoliaMesurements):
    """Monitors the annual consumption."""

    @property
    def unique_id(self) -> str:
        """Return a unique ID to use for this entity."""
        return f"{self.config_entry.entry_id}_annual_consumption"

    @property
    def has_entity_name(self) -> bool:
        """Indicate that entity has name defined."""
        return True

    @property
    def translation_key(self) -> str:
        """Translation key for this entity."""
        return "annual_consumption"

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        total_consumption = sum(
            month[CONSO][LITRE] for month in self.coordinator.data.monthly_consumption
        )
        LOGGER.debug("Annual consumption: %s L", total_consumption)
        return total_consumption if total_consumption > 0 else None

    @property
    def state_class(self) -> str:
        """Return the state_class of the sensor."""
        return SensorStateClass.TOTAL_INCREASING

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit_of_measurement of the sensor."""
        return UnitOfVolume.LITERS

    @property
    def suggested_display_precision(self) -> int:
        """Return the suggested display precision."""
        return 0

    @property
    def icon(self) -> str | None:
        """Set icon."""
        return "mdi:water"


class LastDateSensor(CoordinatorEntity, SensorEntity):
    """Monitors the last date without time."""

    def __init__(self, coordinator, config_entry) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
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
        return f"{self.config_entry.entry_id}_last_date"

    @property
    def has_entity_name(self) -> bool:
        """Indicate that entity has name defined."""
        return True

    @property
    def translation_key(self) -> str:
        """Translation key for this entity."""
        return "last_consumption_date"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        date_str = self.coordinator.data.daily_consumption[LAST_DATA][DATA_DATE]
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        LOGGER.debug("Last date: %s", date_obj.date())
        return date_obj.date().isoformat()

    @property
    def icon(self) -> str | None:
        """Set icon."""
        return "mdi:calendar"
