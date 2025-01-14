"""Config flow for the Shom Maree integration."""

from __future__ import annotations

import voluptuous as vol

from typing import Any

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from .api import CannotConnect, InvalidAuth, ShomMareeAPI
from .const import _LOGGER, CONF_DURATION, CONF_HARBOR_NAME, DOMAIN


STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HARBOR_NAME): str,
        vol.Required(CONF_DURATION): str,
    }
)


class ShomMareeConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Shom."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                api = ShomMareeAPI()
                await api.get_tides(user_input["harbor_name"], user_input["duration"])
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=user_input["harbor_name"], data=user_input
                )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
