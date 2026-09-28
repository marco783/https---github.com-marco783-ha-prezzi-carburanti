"""Data update coordinator for Prezzi Medi Carburanti."""
from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API_URL, DOMAIN, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class PrezziCarburantiCoordinator(DataUpdateCoordinator[dict]):
    """Fetches the national average fuel prices once per interval."""

    def __init__(self, hass: HomeAssistant) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=UPDATE_INTERVAL,
        )

    async def _async_update_data(self) -> dict:
        session = async_get_clientsession(self.hass)
        try:
            async with session.get(API_URL, timeout=15) as resp:
                resp.raise_for_status()
                payload = await resp.json(content_type=None)
        except Exception as err:  # noqa: BLE001 - surfaced as UpdateFailed
            raise UpdateFailed(f"Errore nel recupero prezzi carburanti: {err}") from err

        national = payload.get("national")
        if not national:
            raise UpdateFailed("Risposta API senza campo 'national'")

        return {
            "national": national,
            "date": payload.get("date"),
            "published_at": payload.get("published_at"),
            "source": payload.get("source"),
        }
