"""
Configuration module for n-body simulation.

This module provides configuration management for solar system presets,
simulation parameters, and system settings.
"""

from .solar_system import (
    SolarSystemConfig,
    get_preset_system,
    calculate_orbital_velocity,
    calculate_orbital_period,
    PLANET_DATA,
    AU,
    SOLAR_MASS,
    EARTH_MASS
)
from .parameters import (
    SimulationParameters,
    create_default_config_file,
    load_config_from_file
)

__all__ = [
    'SolarSystemConfig',
    'get_preset_system',
    'calculate_orbital_velocity',
    'calculate_orbital_period',
    'SimulationParameters',
    'create_default_config_file',
    'load_config_from_file',
    'PLANET_DATA',
    'AU',
    'SOLAR_MASS',
    'EARTH_MASS'
]