"""Config flow for Waste Collection Kranj integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol # type: ignore
import aiohttp # type: ignore

from homeassistant import config_entries # type: ignore
from homeassistant.core import HomeAssistant # type: ignore
from homeassistant.data_entry_flow import FlowResult # type: ignore
from homeassistant.exceptions import HomeAssistantError # type: ignore

from .const import DOMAIN, BASE_URL

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("hsmid"): str,
        vol.Optional("name", default="Waste Collection Kranj"): str,
    }
)

async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""

    # Test the connection and data
    async with aiohttp.ClientSession() as session:
        params = {
            "a": "komunalakranj",
            "hsMid": data["hsmid"],
            "stDni": "30",
            "_": "1"
        }
        
        async with session.get(BASE_URL, params=params) as response:
            if response.status != 200:
                raise InvalidAuth

    return {"title": f"Waste Collection Kranj {data['hsmid']}"}

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Waste Collection Kranj."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""

class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""