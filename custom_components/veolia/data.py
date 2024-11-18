"""Custom types for Veolia."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.config_entries import ConfigEntry

if TYPE_CHECKING:
    from veolia_api import VeoliaAPI

    from homeassistant.loader import Integration

    from .coordinator import VeoliaDataUpdateCoordinator

type VeoliaConfigEntry = ConfigEntry[VeoliaData]


@dataclass
class VeoliaData:
    """Data for the Veolia integration."""

    client: VeoliaAPI
    coordinator: VeoliaDataUpdateCoordinator
    integration: Integration
