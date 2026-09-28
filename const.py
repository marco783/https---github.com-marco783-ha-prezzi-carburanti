"""Constants for the Prezzi Medi Carburanti integration."""
from datetime import timedelta

DOMAIN = "prezzi_carburanti"
API_URL = "https://mappacarburanti.it/api/prezzi/today.json"
UPDATE_INTERVAL = timedelta(hours=6)

# key in the API's "national" object -> (sensor slug, friendly name, icon)
FUEL_TYPES = {
    "benzina": ("benzina", "Benzina", "mdi:gas-station"),
    "gasolio": ("gasolio", "Gasolio", "mdi:gas-station"),
    "gpl": ("gpl", "GPL", "mdi:gas-station-outline"),
    "metano": ("metano", "Metano", "mdi:gas-cylinder"),
}
