"""Sensor platform for Prezzi Medi Carburanti."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, FUEL_TYPES
from .coordinator import PrezziCarburantiCoordinator


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: PrezziCarburantiCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        FuelPriceSensor(coordinator, entry, fuel_key)
        for fuel_key in FUEL_TYPES
        if fuel_key in (coordinator.data or {}).get("national", {})
    )


class FuelPriceSensor(CoordinatorEntity[PrezziCarburantiCoordinator], SensorEntity):
    """Average national price for one fuel type, in EUR/L."""

    _attr_has_entity_name = True
    _attr_native_unit_of_measurement = "EUR/L"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_suggested_display_precision = 3

    def __init__(
        self,
        coordinator: PrezziCarburantiCoordinator,
        entry: ConfigEntry,
        fuel_key: str,
    ) -> None:
        super().__init__(coordinator)
        _slug, name, icon = FUEL_TYPES[fuel_key]
        self._fuel_key = fuel_key
        self._attr_name = name
        self._attr_icon = icon
        self._attr_unique_id = f"{entry.entry_id}_{fuel_key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Prezzi Medi Carburanti",
            manufacturer="mappacarburanti.it",
            model="Media nazionale giornaliera",
        )

    @property
    def native_value(self) -> float | None:
        fuel = (self.coordinator.data or {}).get("national", {}).get(self._fuel_key)
        return fuel.get("avg") if fuel else None

    @property
    def extra_state_attributes(self) -> dict:
        data = self.coordinator.data or {}
        fuel = data.get("national", {}).get(self._fuel_key, {})
        return {
            "min": fuel.get("min"),
            "max": fuel.get("max"),
            "stazioni_rilevate": fuel.get("count"),
            "data_rilevazione": data.get("date"),
            "pubblicato_il": data.get("published_at"),
            "fonte": data.get("source"),
        }
