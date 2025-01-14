"""Sensor for the Shom Maree integration."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import COORDINATOR, DOMAIN
from .coordinator import ShomMareeConfigEntry

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ShomMareeConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensors for the Shom Maree integration."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id][COORDINATOR]
    sensors = []

    # Parcourir les données et créer un capteur pour chaque parc relais
    day = 1
    for date in coordinator.data:
        sensors.append(ShomMareeSensor(config_entry.title, date, day, coordinator))
        day += 1

    async_add_entities(sensors, True)


class ShomMareeSensor(SensorEntity):
    """Sensor for a specific harbor."""

    def __init__(self, harbor_name, date, day, coordinator) -> None:
        """Initialize the sensor."""
        self._harbor_name = harbor_name
        self._date = date
        self._day = day

        self.coordinator = coordinator

    @property
    def name(self):
        """Name of the sensor."""
        return f"Shom maree {self._harbor_name} day {self._day}"

    @property
    def unique_id(self):
        """Unique identifier for the entity."""
        return f"{self._harbor_name}_{self._date}_day_{self._day}"

    @property
    def state(self):
        """Main state (tide date)."""
        return self._date

    @property
    def extra_state_attributes(self):
        """Additional attributes."""
        data = {}

        tides = self._get_tides_data()

        if tides:
            i = 1
            for tide in tides:
                nb = (i + 1) // 2

                data[f"tide{nb}_{tide['type']}_time"] = tide["time"]
                data[f"tide{nb}_{tide['type']}_height"] = tide["height"]
                data[f"tide{nb}_{tide['type']}_coefficient"] = tide["coefficient"]

                i += 1

        return data

    @property
    def icon(self):
        """Icon for the sensor."""
        return "mdi:waves"

    @property
    def device_info(self):
        """Return device info to group entities under a device."""
        return {
            "identifiers": {(DOMAIN, self._harbor_name)},
            "name": f"Port {self._harbor_name}",
            "manufacturer": "SHOM",
            "model": "Tide Station",
        }

    def _get_tides_data(self):
        """Retrieve data for this harbor."""
        if len(self.coordinator.data) > 0:
            return self.coordinator.data[self._date]
        return None

    async def async_update(self):
        """Ask the coordinator to update the data."""
        await self.coordinator.async_request_refresh()
