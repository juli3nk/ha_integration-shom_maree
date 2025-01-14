"""ShomMareeAPI class for interacting with
the SHOM (Service Hydrographique et Océanographique de la Marine) API.

It retrieves tide data such as high and low tides,
including times, heights,
and coefficients for a specific harbor over a given duration.

Usage:
    api = ShomMareeAPI()
    tides = await api.get_tides(harbor_name="Your Harbor", duration=7)

Classes:
    - ShomMareeAPI: Represents the API client for fetching tide data.

"""

import aiohttp

from datetime import datetime


class ShomMareeAPI:
    """API client for retrieving tide data from the SHOM service."""

    def __init__(self) -> None:
        """Initialize the API client."""
        self.base_url = "https://services.data.shom.fr"
        self.api_key = "b2q8lrcdl4s04cbabsj4nhcb"

    async def get_tides(self, harbor_name: str, duration: int):
        """Fetch tide data for a specific harbor and duration.

        Args:
            harbor_name (str): The name of the harbor for which to retrieve tide data.
            duration (int): The number of days to retrieve tide data for.

        Returns:
            dict: A dictionary containing tide data by date.

        """

        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        utc = "standard"
        correlation = 1

        headers = {
            "Referer": "https://maree.shom.fr",
        }

        async with (
            aiohttp.ClientSession() as session,
            session.get(
                f"{self.base_url}/{self.api_key}/hdm/spm/hlt",
                params={
                    "harborName": harbor_name,
                    "duration": duration,
                    "date": date,
                    "utc": utc,
                    "correlation": correlation,
                },
                headers=headers,
            ) as response,
        ):
            response.raise_for_status()
            return await response.json()


class CannotConnect(Exception):
    """Error to indicate we cannot connect."""


class InvalidAuth(Exception):
    """Error to indicate there is invalid auth."""
