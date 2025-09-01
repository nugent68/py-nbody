"""
Celestial body class for n-body simulation.
"""
from typing import Optional
from .vector3d import Vector3D


class Body:
    """
    Represents a celestial body with mass, position, velocity, and acceleration.
    """
    
    def __init__(self, 
                 mass: float,
                 position: Vector3D,
                 velocity: Vector3D,
                 name: str = "Unnamed Body",
                 color: str = "blue",
                 radius: float = 1.0):
        """
        Initialize a celestial body.
        
        Args:
            mass: Mass of the body (kg)
            position: Initial position vector (m)
            velocity: Initial velocity vector (m/s)
            name: Name of the body for identification
            color: Color for visualization
            radius: Visual radius for plotting (not used in physics)
        """
        self.mass = float(mass)
        self.position = position
        self.velocity = velocity
        self.acceleration = Vector3D(0, 0, 0)
        self.name = name
        self.color = color
        self.radius = float(radius)
        
        # For tracking trajectory
        self.trajectory = [position]
        
        # Physical properties
        self.kinetic_energy = 0.0
        self.potential_energy = 0.0
    
    def update_position(self, dt: float) -> None:
        """
        Update position based on current velocity.
        
        Args:
            dt: Time step (s)
        """
        self.position = self.position + self.velocity * dt
        self.trajectory.append(Vector3D(self.position.x, self.position.y, self.position.z))
    
    def update_velocity(self, dt: float) -> None:
        """
        Update velocity based on current acceleration.
        
        Args:
            dt: Time step (s)
        """
        self.velocity = self.velocity + self.acceleration * dt
    
    def apply_force(self, force: Vector3D) -> None:
        """
        Apply a force to the body, updating acceleration.
        
        Args:
            force: Force vector (N)
        """
        self.acceleration = force / self.mass
    
    def add_force(self, force: Vector3D) -> None:
        """
        Add a force to the existing acceleration.
        
        Args:
            force: Additional force vector (N)
        """
        self.acceleration = self.acceleration + (force / self.mass)
    
    def reset_forces(self) -> None:
        """Reset acceleration to zero (call before calculating new forces)."""
        self.acceleration = Vector3D(0, 0, 0)
    
    def calculate_kinetic_energy(self) -> float:
        """
        Calculate kinetic energy of the body.
        
        Returns:
            Kinetic energy (J)
        """
        v_squared = self.velocity.magnitude_squared()
        self.kinetic_energy = 0.5 * self.mass * v_squared
        return self.kinetic_energy
    
    def distance_to(self, other: 'Body') -> float:
        """
        Calculate distance to another body.
        
        Args:
            other: Another Body object
            
        Returns:
            Distance (m)
        """
        return self.position.distance_to(other.position)
    
    def momentum(self) -> Vector3D:
        """
        Calculate momentum vector.
        
        Returns:
            Momentum vector (kg⋅m/s)
        """
        return self.velocity * self.mass
    
    def angular_momentum(self, origin: Vector3D = None) -> Vector3D:
        """
        Calculate angular momentum about a point.
        
        Args:
            origin: Point to calculate angular momentum about (default: origin)
            
        Returns:
            Angular momentum vector (kg⋅m²/s)
        """
        if origin is None:
            origin = Vector3D(0, 0, 0)
        
        r = self.position - origin
        p = self.momentum()
        return r.cross(p)
    
    def clear_trajectory(self) -> None:
        """Clear the trajectory history."""
        self.trajectory = [Vector3D(self.position.x, self.position.y, self.position.z)]
    
    def get_trajectory_arrays(self):
        """
        Get trajectory as separate x, y, z arrays for plotting.
        
        Returns:
            Tuple of (x_array, y_array, z_array)
        """
        if not self.trajectory:
            return [], [], []
        
        x_coords = [pos.x for pos in self.trajectory]
        y_coords = [pos.y for pos in self.trajectory]
        z_coords = [pos.z for pos in self.trajectory]
        
        return x_coords, y_coords, z_coords
    
    def __str__(self) -> str:
        """String representation."""
        return (f"Body(name='{self.name}', mass={self.mass:.2e}, "
                f"pos={self.position}, vel={self.velocity})")
    
    def __repr__(self) -> str:
        """Representation."""
        return self.__str__()