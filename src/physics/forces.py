"""
Force calculation functions for n-body gravitational simulation.
"""
import numpy as np
from typing import List
from .body import Body
from .vector3d import Vector3D


# Gravitational constant (m³/kg⋅s²)
G = 6.67430e-11


class GravitationalForceCalculator:
    """
    Calculates gravitational forces between all bodies in an n-body system.
    """
    
    def __init__(self, gravitational_constant: float = G, softening_length: float = 0.0):
        """
        Initialize the force calculator.
        
        Args:
            gravitational_constant: Gravitational constant (default: standard G)
            softening_length: Softening parameter to avoid singularities (m)
        """
        self.G = gravitational_constant
        self.softening_length = softening_length
        self.softening_squared = softening_length ** 2
    
    def calculate_forces(self, bodies: List[Body]) -> None:
        """
        Calculate gravitational forces between all bodies and update their accelerations.
        
        Uses Newton's law of universal gravitation:
        F = G * m1 * m2 / r² * r̂
        
        Args:
            bodies: List of Body objects
        """
        n = len(bodies)
        
        # Reset all forces to zero
        for body in bodies:
            body.reset_forces()
        
        # Calculate pairwise forces
        for i in range(n):
            for j in range(i + 1, n):
                force = self._calculate_pairwise_force(bodies[i], bodies[j])
                
                # Apply Newton's third law: F_ij = -F_ji
                bodies[i].add_force(force)
                bodies[j].add_force(-force)
    
    def _calculate_pairwise_force(self, body1: Body, body2: Body) -> Vector3D:
        """
        Calculate gravitational force between two bodies.
        
        Args:
            body1: First body
            body2: Second body
            
        Returns:
            Force vector acting on body1 due to body2
        """
        # Vector from body1 to body2
        r_vector = body2.position - body1.position
        
        # Distance between bodies
        r_squared = r_vector.magnitude_squared() + self.softening_squared
        r = np.sqrt(r_squared)
        
        # Avoid division by zero
        if r < 1e-10:
            return Vector3D(0, 0, 0)
        
        # Unit vector pointing from body1 to body2
        r_hat = r_vector / r
        
        # Gravitational force magnitude
        force_magnitude = self.G * body1.mass * body2.mass / r_squared
        
        # Force vector (pointing from body1 toward body2)
        force = r_hat * force_magnitude
        
        return force
    
    def calculate_potential_energy(self, bodies: List[Body]) -> float:
        """
        Calculate total gravitational potential energy of the system.
        
        U = -G * Σ(m_i * m_j / r_ij) for all pairs i < j
        
        Args:
            bodies: List of Body objects
            
        Returns:
            Total potential energy (J)
        """
        potential_energy = 0.0
        n = len(bodies)
        
        for i in range(n):
            for j in range(i + 1, n):
                r = bodies[i].distance_to(bodies[j])
                if r > 1e-10:  # Avoid division by zero
                    potential_energy -= self.G * bodies[i].mass * bodies[j].mass / r
        
        return potential_energy
    
    def calculate_total_energy(self, bodies: List[Body]) -> tuple:
        """
        Calculate total kinetic and potential energy of the system.
        
        Args:
            bodies: List of Body objects
            
        Returns:
            Tuple of (kinetic_energy, potential_energy, total_energy)
        """
        kinetic_energy = sum(body.calculate_kinetic_energy() for body in bodies)
        potential_energy = self.calculate_potential_energy(bodies)
        total_energy = kinetic_energy + potential_energy
        
        return kinetic_energy, potential_energy, total_energy
    
    def calculate_center_of_mass(self, bodies: List[Body]) -> Vector3D:
        """
        Calculate center of mass of the system.
        
        Args:
            bodies: List of Body objects
            
        Returns:
            Center of mass position vector
        """
        total_mass = sum(body.mass for body in bodies)
        if total_mass == 0:
            return Vector3D(0, 0, 0)
        
        com_x = sum(body.mass * body.position.x for body in bodies) / total_mass
        com_y = sum(body.mass * body.position.y for body in bodies) / total_mass
        com_z = sum(body.mass * body.position.z for body in bodies) / total_mass
        
        return Vector3D(com_x, com_y, com_z)
    
    def calculate_total_momentum(self, bodies: List[Body]) -> Vector3D:
        """
        Calculate total linear momentum of the system.
        
        Args:
            bodies: List of Body objects
            
        Returns:
            Total momentum vector
        """
        total_momentum = Vector3D(0, 0, 0)
        for body in bodies:
            total_momentum = total_momentum + body.momentum()
        
        return total_momentum
    
    def calculate_total_angular_momentum(self, bodies: List[Body], 
                                       origin: Vector3D = None) -> Vector3D:
        """
        Calculate total angular momentum of the system about a point.
        
        Args:
            bodies: List of Body objects
            origin: Point to calculate angular momentum about (default: origin)
            
        Returns:
            Total angular momentum vector
        """
        if origin is None:
            origin = Vector3D(0, 0, 0)
        
        total_angular_momentum = Vector3D(0, 0, 0)
        for body in bodies:
            total_angular_momentum = total_angular_momentum + body.angular_momentum(origin)
        
        return total_angular_momentum


def create_force_calculator(method: str = "standard", **kwargs) -> GravitationalForceCalculator:
    """
    Factory function to create force calculator with different configurations.
    
    Args:
        method: Type of force calculation ('standard', 'softened')
        **kwargs: Additional parameters for the force calculator
        
    Returns:
        GravitationalForceCalculator instance
    """
    if method == "standard":
        return GravitationalForceCalculator(**kwargs)
    elif method == "softened":
        # Use softening length to avoid singularities
        softening = kwargs.get('softening_length', 1e6)  # 1000 km default
        return GravitationalForceCalculator(softening_length=softening, **kwargs)
    else:
        raise ValueError(f"Unknown force calculation method: {method}")