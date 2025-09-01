"""
Physics module for n-body gravitational simulation.

This module provides the core physics classes and functions for simulating
gravitational interactions between celestial bodies.
"""

from .vector3d import Vector3D
from .body import Body
from .integrators import (
    Integrator, 
    EulerIntegrator, 
    RK4Integrator, 
    LeapfrogIntegrator,
    get_integrator
)
from .forces import GravitationalForceCalculator, create_force_calculator, G
from .engine import PhysicsEngine

__all__ = [
    'Vector3D',
    'Body',
    'Integrator',
    'EulerIntegrator',
    'RK4Integrator', 
    'LeapfrogIntegrator',
    'get_integrator',
    'GravitationalForceCalculator',
    'create_force_calculator',
    'PhysicsEngine',
    'G'
]