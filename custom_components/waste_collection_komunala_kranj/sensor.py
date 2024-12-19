"""Waste Collection Komunala Kranj sensor platform."""
from datetime import datetime, timedelta
import logging
import xml.etree.ElementTree as ET

import aiohttp
import async_timeout

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, BASE_URL

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Waste Collection Komunala Kranj sensor from config entry."""
    name = config_entry.data["name"]
    hsmid = config_entry.data["hsmid"]

    async_add_entities([WasteCollectionSensor(hass, name, hsmid)], True)

class WasteCollectionSensor(SensorEntity):
    """Representation of a Waste Collection sensor."""

    def __init__(self, hass, name, hsmid):
        """Initialize the sensor."""
        self.hass = hass
        self._name = name
        self._hsmid = hsmid
        self._state = 0
        self._available = True
        self._attributes = {
            "collections": [],
            "next_collection": None,
            "last_updated": None
        }
        _LOGGER.debug("Sensor initialized with name: %s", self._name)

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def available(self):
        """Return True if entity is available."""
        return self._available

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"waste_collection_komunala_kranj_{self._hsmid}"

    async def async_update(self):
        """Fetch new state data for the sensor."""
        _LOGGER.debug("Starting sensor update")
        
        params = {
            "a": "komunalakranj",
            "hsMid": self._hsmid,
            "stDni": "30",
            "_": str(int(datetime.now().timestamp() * 1000))
        }

        try:
            async with aiohttp.ClientSession() as session:
                _LOGGER.debug("Fetching data with params: %s", params)
                async with async_timeout.timeout(10):
                    async with session.get(BASE_URL, params=params) as response:
                        _LOGGER.debug("Response status: %s", response.status)
                        
                        if response.status != 200:
                            self._available = False
                            _LOGGER.error("Failed to get data, status code: %s", response.status)
                            return

                        text = await response.text()
                        _LOGGER.debug("Received data: %s", text)

                        # Parse XML response
                        root = ET.fromstring(text)
                        collections = []
                        
                        # XML namespace from your example
                        ns = {'ns': 'http://tempuri.org/'}
                        
                        for collection in root.findall('.//ns:DanOdvoza', ns):
                            collection_data = {
                                "date": collection.find('ns:Datum', ns).text,
                                "type": collection.find('ns:VrstaZabojnika', ns).text,
                                "description": collection.find('ns:VrstaOdpadka', ns).text,
                                "color": collection.find('ns:BarvaZabojnika', ns).text.strip()
                            }
                            collections.append(collection_data)
                            _LOGGER.debug("Added collection: %s", collection_data)

                        # Update state and attributes
                        self._state = len(collections)
                        self._attributes["collections"] = collections
                        self._attributes["next_collection"] = collections[0] if collections else None
                        self._attributes["last_updated"] = datetime.now().isoformat()
                        self._available = True

                        # Schedule notification for tomorrow's collections
                        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y")
                        tomorrow_collections = [c for c in collections if c["date"] == tomorrow]

                        if tomorrow_collections:
                            notification_time = datetime.now().replace(
                                hour=20, minute=0, second=0, microsecond=0
                            )
                            
                            for collection in tomorrow_collections:
                                waste_type_names = {
                                    "ODPADNA EMBALAŽA": "rumeno",
                                    "BIOLOŠKI ODPADKI": "rjavo",
                                    "MEŠANI KOMUNALNI ODPADKI": "zeleno"
                                }
                                waste_type = waste_type_names.get(collection['description'], collection['description'])
                                
                                await self.hass.services.async_call(
                                    "notify",
                                    "mobile_app",
                                    {
                                        "title": "Odvoz smeti jutri",
                                        "message": f"Odnesi smeti v {waste_type} kanto, ker je jutri odvoz",
                                        "data": {
                                            "color": collection['color']
                                        }
                                    },
                                    scheduled_time=notification_time
                                )

        except Exception as error:
            self._available = False
            _LOGGER.error("Error fetching data: %s", error)