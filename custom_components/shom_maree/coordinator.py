"""Coordinator for the Shom Maree integration."""

from __future__ import annotations

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import ShomMareeAPI
from .const import _LOGGER, DOMAIN, UPDATE_INTERVAL

type ShomMareeConfigEntry = ConfigEntry[ShomMareeDataUpdateCoordinator]


class ShomMareeDataUpdateCoordinator(DataUpdateCoordinator):
    """Coordinator for retrieving and updating Shom tide data."""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ShomMareeConfigEntry
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )

        self.config_entry = config_entry

    async def _async_update_data(self):
        """Retrieve data from the Shom API."""
        try:
            api = ShomMareeAPI()
            raw_data = await api.get_tides(
                self.config_entry.data.get("harbor_name"),
                self.config_entry.data.get("duration"),
            )
            return self._process_raw_data(raw_data)
        except Exception as err:
            _LOGGER.error(
                "Erreur lors de la mise à jour des données Shom marees: %s", err
            )
            raise

    @staticmethod
    def _process_raw_data(raw_data):
        """Transform raw API data into a structured format."""
        data = {}
        for date, tides in raw_data.items():
            data[date] = [
                {
                    "type": tide[0].split(".")[1],  # "high" or "low"
                    "time": tide[1],
                    "height": tide[2],
                    "coefficient": tide[3],
                }
                for tide in tides
                if tide[0] != "tide.none"
            ]
        return data
