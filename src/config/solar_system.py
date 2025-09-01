"""
Solar system configuration with realistic masses and orbital parameters.
"""
import math
from typing import List, Dict, Any
from ..physics import Body, Vector3D


# Physical constants and conversion factors
AU = 1.496e11  # Astronomical Unit in meters
SOLAR_MASS = 1.989e30  # Solar mass in kg
EARTH_MASS = 5.972e24  # Earth mass in kg
DAY = 86400  # Day in seconds
YEAR = 365.25 * DAY  # Year in seconds

# Planet data: [mass_ratio_to_earth, distance_au, orbital_period_years, color, radius_km]
PLANET_DATA = {
    'mercury': [0.0553, 0.387, 0.241, 'gray', 2439.7],
    'venus': [0.815, 0.723, 0.615, 'orange', 6051.8],
    'earth': [1.0, 1.0, 1.0, 'blue', 6371.0],
    'mars': [0.107, 1.524, 1.881, 'red', 3389.5],
    'jupiter': [317.8, 5.204, 11.862, 'brown', 69911],
    'saturn': [95.2, 9.573, 29.457, 'gold', 58232],
    'uranus': [14.5, 19.165, 84.017, 'cyan', 25362],
    'neptune': [17.1, 30.178, 164.791, 'darkblue', 24622]
}


class SolarSystemConfig:
    """
    Configuration class for creating solar system scenarios.
    """
    
    def __init__(self, scale_factor: float = 1.0, time_scale: float = 1.0):
        """
        Initialize solar system configuration.
        
        Args:
            scale_factor: Scale factor for distances (1.0 = real scale)
            time_scale: Scale factor for time (1.0 = real time)
        """
        self.scale_factor = scale_factor
        self.time_scale = time_scale
        self.G_scaled = 6.67430e-11 * (time_scale ** 2)
    
    def create_sun(self) -> Body:
        """
        Create the Sun at the origin.
        
        Returns:
            Body object representing the Sun
        """
        return Body(
            mass=SOLAR_MASS,
            position=Vector3D(0, 0, 0),
            velocity=Vector3D(0, 0, 0),
            name="Sun",
            color="yellow",
            radius=696340  # km
        )
    
    def create_planet(self, planet_name: str, 
                     initial_angle: float = 0.0,
                     inclination: float = 0.0) -> Body:
        """
        Create a planet with realistic orbital parameters.
        
        Args:
            planet_name: Name of the planet (lowercase)
            initial_angle: Initial orbital angle in radians
            inclination: Orbital inclination in radians
            
        Returns:
            Body object representing the planet
        """
        if planet_name.lower() not in PLANET_DATA:
            raise ValueError(f"Unknown planet: {planet_name}")
        
        data = PLANET_DATA[planet_name.lower()]
        mass_ratio, distance_au, period_years, color, radius_km = data
        
        # Calculate orbital parameters
        mass = mass_ratio * EARTH_MASS
        distance = distance_au * AU * self.scale_factor
        period = period_years * YEAR / self.time_scale
        
        # Calculate orbital velocity using circular orbit approximation
        # v = 2π * r / T
        orbital_speed = 2 * math.pi * distance / period
        
        # Position (starting at initial_angle)
        x = distance * math.cos(initial_angle)
        y = distance * math.sin(initial_angle) * math.cos(inclination)
        z = distance * math.sin(initial_angle) * math.sin(inclination)
        position = Vector3D(x, y, z)
        
        # Velocity (perpendicular to position for circular orbit)
        vx = -orbital_speed * math.sin(initial_angle)
        vy = orbital_speed * math.cos(initial_angle) * math.cos(inclination)
        vz = orbital_speed * math.cos(initial_angle) * math.sin(inclination)
        velocity = Vector3D(vx, vy, vz)
        
        return Body(
            mass=mass,
            position=position,
            velocity=velocity,
            name=planet_name.capitalize(),
            color=color,
            radius=radius_km
        )
    
    def create_inner_solar_system(self) -> List[Body]:
        """
        Create the inner solar system (Sun + Mercury, Venus, Earth, Mars).
        
        Returns:
            List of Body objects
        """
        bodies = [self.create_sun()]
        
        # Add inner planets with different starting angles
        planets = ['mercury', 'venus', 'earth', 'mars']
        angles = [0, math.pi/2, math.pi, 3*math.pi/2]  # Spread them out
        
        for planet, angle in zip(planets, angles):
            bodies.append(self.create_planet(planet, initial_angle=angle))
        
        return bodies
    
    def create_full_solar_system(self) -> List[Body]:
        """
        Create the full solar system (Sun + all 8 planets).
        
        Returns:
            List of Body objects
        """
        bodies = [self.create_sun()]
        
        # Add all planets with different starting angles
        planets = list(PLANET_DATA.keys())
        angles = [i * 2 * math.pi / len(planets) for i in range(len(planets))]
        
        for planet, angle in zip(planets, angles):
            bodies.append(self.create_planet(planet, initial_angle=angle))
        
        return bodies
    
    def create_earth_moon_system(self) -> List[Body]:
        """
        Create Earth-Moon system.
        
        Returns:
            List of Body objects
        """
        # Earth
        earth = Body(
            mass=EARTH_MASS,
            position=Vector3D(0, 0, 0),
            velocity=Vector3D(0, 0, 0),
            name="Earth",
            color="blue",
            radius=6371
        )
        
        # Moon orbital parameters
        moon_distance = 384400e3 * self.scale_factor  # 384,400 km
        moon_mass = 7.342e22  # kg
        moon_period = 27.3 * DAY / self.time_scale  # 27.3 days
        moon_speed = 2 * math.pi * moon_distance / moon_period
        
        moon = Body(
            mass=moon_mass,
            position=Vector3D(moon_distance, 0, 0),
            velocity=Vector3D(0, moon_speed, 0),
            name="Moon",
            color="gray",
            radius=1737
        )
        
        return [earth, moon]
    
    def create_custom_system(self, config: Dict[str, Any]) -> List[Body]:
        """
        Create a custom system from configuration dictionary.
        
        Args:
            config: Dictionary with body configurations
            
        Returns:
            List of Body objects
        """
        bodies = []
        
        for body_config in config.get('bodies', []):
            body = Body(
                mass=body_config['mass'],
                position=Vector3D(*body_config['position']),
                velocity=Vector3D(*body_config['velocity']),
                name=body_config.get('name', 'Unnamed'),
                color=body_config.get('color', 'blue'),
                radius=body_config.get('radius', 1.0)
            )
            bodies.append(body)
        
        return bodies


def get_preset_system(preset_name: str, **kwargs) -> List[Body]:
    """
    Get a preset solar system configuration.
    
    Args:
        preset_name: Name of the preset ('inner', 'full', 'earth_moon')
        **kwargs: Additional arguments for SolarSystemConfig
        
    Returns:
        List of Body objects
        
    Raises:
        ValueError: If preset_name is not recognized
    """
    config = SolarSystemConfig(**kwargs)
    
    if preset_name == 'inner':
        return config.create_inner_solar_system()
    elif preset_name == 'full':
        return config.create_full_solar_system()
    elif preset_name == 'earth_moon':
        return config.create_earth_moon_system()
    else:
        raise ValueError(f"Unknown preset: {preset_name}. "
                        f"Available presets: 'inner', 'full', 'earth_moon'")


def calculate_orbital_velocity(central_mass: float, distance: float, 
                             gravitational_constant: float = 6.67430e-11) -> float:
    """
    Calculate circular orbital velocity.
    
    Args:
        central_mass: Mass of central body (kg)
        distance: Orbital distance (m)
        gravitational_constant: Gravitational constant
        
    Returns:
        Orbital velocity (m/s)
    """
    return math.sqrt(gravitational_constant * central_mass / distance)


def calculate_orbital_period(central_mass: float, distance: float,
                           gravitational_constant: float = 6.67430e-11) -> float:
    """
    Calculate orbital period using Kepler's third law.
    
    Args:
        central_mass: Mass of central body (kg)
        distance: Orbital distance (m)
        gravitational_constant: Gravitational constant
        
    Returns:
        Orbital period (s)
    """
    return 2 * math.pi * math.sqrt(distance**3 / (gravitational_constant * central_mass))