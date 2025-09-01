"""
3D Vector class for position, velocity, and acceleration calculations.
"""
import numpy as np
from typing import Union


class Vector3D:
    """
    A 3D vector class with common vector operations for physics calculations.
    """
    
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        """
        Initialize a 3D vector.
        
        Args:
            x: X component
            y: Y component  
            z: Z component
        """
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
    
    @classmethod
    def from_array(cls, arr: np.ndarray) -> 'Vector3D':
        """Create Vector3D from numpy array."""
        return cls(arr[0], arr[1], arr[2])
    
    def to_array(self) -> np.ndarray:
        """Convert to numpy array."""
        return np.array([self.x, self.y, self.z])
    
    def __add__(self, other: 'Vector3D') -> 'Vector3D':
        """Vector addition."""
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: 'Vector3D') -> 'Vector3D':
        """Vector subtraction."""
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar: float) -> 'Vector3D':
        """Scalar multiplication."""
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __rmul__(self, scalar: float) -> 'Vector3D':
        """Right scalar multiplication."""
        return self.__mul__(scalar)
    
    def __truediv__(self, scalar: float) -> 'Vector3D':
        """Scalar division."""
        return Vector3D(self.x / scalar, self.y / scalar, self.z / scalar)
    
    def __neg__(self) -> 'Vector3D':
        """Vector negation."""
        return Vector3D(-self.x, -self.y, -self.z)
    
    def magnitude(self) -> float:
        """Calculate vector magnitude."""
        return np.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def magnitude_squared(self) -> float:
        """Calculate squared magnitude (more efficient when only comparing)."""
        return self.x**2 + self.y**2 + self.z**2
    
    def normalize(self) -> 'Vector3D':
        """Return normalized vector (unit vector)."""
        mag = self.magnitude()
        if mag == 0:
            return Vector3D(0, 0, 0)
        return self / mag
    
    def dot(self, other: 'Vector3D') -> float:
        """Dot product."""
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other: 'Vector3D') -> 'Vector3D':
        """Cross product."""
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
    def distance_to(self, other: 'Vector3D') -> float:
        """Calculate distance to another vector."""
        return (self - other).magnitude()
    
    def __str__(self) -> str:
        """String representation."""
        return f"Vector3D({self.x:.6f}, {self.y:.6f}, {self.z:.6f})"
    
    def __repr__(self) -> str:
        """Representation."""
        return self.__str__()
    
    def __eq__(self, other: 'Vector3D') -> bool:
        """Equality comparison with small tolerance."""
        tolerance = 1e-10
        return (abs(self.x - other.x) < tolerance and 
                abs(self.y - other.y) < tolerance and 
                abs(self.z - other.z) < tolerance)