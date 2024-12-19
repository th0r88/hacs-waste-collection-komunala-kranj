"""Config flow for Waste Collection Komunala Kranj."""
import logging
import voluptuous as vol
import aiohttp

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import CONF_NAME

from .const import DOMAIN, DEFAULT_NAME

_LOGGER = logging.getLogger(__name__)

class WasteCollectionFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle a flow initiated by the user."""
        errors = {}

        if user_input is not None:
            try:
                # Validate the hsMid by making a test API call
                async with aiohttp.ClientSession() as session:
                    params = {
                        "a": "komunalakranj",
                        "hsMid": user_input["hsmid"],
                        "stDni": "30",
                        "_": "1"
                    }
                    async with session.get(
                        "https://gis.komunala-kranj.si/ddmoduli/EkoloskiOtoki.asmx/GetKoledarOdvozov",
                        params=params
                    ) as response:
                        if response.status == 200:
                            # Create entry if hsMid is valid
                            return self.async_create_entry(
                                title=user_input.get(CONF_NAME, DEFAULT_NAME),
                                data=user_input
                            )
                        else:
                            errors["base"] = "invalid_hsmid"
            except aiohttp.ClientError:
                errors["base"] = "cannot_connect"
            except Exception as error:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        # Show configuration form
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("hsmid"): str,
                    vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
                }
            ),
            errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)

class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for the integration."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        errors = {}

        if user_input is not None:
            try:
                # Validate the new hsMid
                async with aiohttp.ClientSession() as session:
                    params = {
                        "a": "komunalakranj",
                        "hsMid": user_input["hsmid"],
                        "stDni": "30",
                        "_": "1"
                    }
                    async with session.get(
                        "https://gis.komunala-kranj.si/ddmoduli/EkoloskiOtoki.asmx/GetKoledarOdvozov",
                        params=params
                    ) as response:
                        if response.status == 200:
                            return self.async_create_entry(title="", data=user_input)
                        else:
                            errors["base"] = "invalid_hsmid"
            except aiohttp.ClientError:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "hsmid",
                        default=self.config_entry.data.get("hsmid", "")
                    ): str,
                    vol.Optional(
                        CONF_NAME,
                        default=self.config_entry.data.get(CONF_NAME, DEFAULT_NAME)
                    ): str,
                }
            ),
            errors=errors
        )