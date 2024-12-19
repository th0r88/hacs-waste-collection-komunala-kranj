"""Constants for the Waste Collection Kranj integration."""
DOMAIN = "waste_collection_kranj"

DEFAULT_NAME = "Waste Collection Kranj"
DEFAULT_UPDATE_INTERVAL = 3600  # 1 hour in seconds

# Configuration constants
CONF_HSMID = "hsmid"

# API constants
BASE_URL = "https://gis.komunala-kranj.si/ddmoduli/EkoloskiOtoki.asmx/GetKoledarOdvozov"

# Color mapping based on waste type
COLORS = {
    "EMB": "#f9df2e",  # Yellow
    "BIO": "#74421f",  # Brown
    "MKO": "#83c441"   # Green
}

WASTE_TYPES = {
    "EMB": "Waste Packaging",
    "BIO": "Biological Waste",
    "MKO": "Mixed Waste"
}