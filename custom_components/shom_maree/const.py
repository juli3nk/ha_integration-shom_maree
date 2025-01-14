"""Constants for the Shom Maree integration."""

import logging

from typing import Final


DOMAIN = "shom_maree"

_LOGGER = logging.getLogger(__name__)

CONF_HARBOR_NAME: Final = "harbor_name"
CONF_DURATION: Final = "duration"

COORDINATOR = "coordinator"
UPDATE_INTERVAL = 60
