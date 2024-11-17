"""VeoliaEntity class."""

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfVolume
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, NAME


class VeoliaMesurements(CoordinatorEntity, SensorEntity):
    """Representation of a Veolia entity."""

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
    def state_class(self) -> str:
        """Return the state_class of the sensor."""
        return SensorStateClass.TOTAL_INCREASING

    @property
    def device_class(self) -> str:
        """Return the device_class of the sensor."""
        return SensorDeviceClass.WATER

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit_of_measurement of the sensor."""
        return UnitOfVolume.LITERS
