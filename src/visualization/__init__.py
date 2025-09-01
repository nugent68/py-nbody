"""
Visualization module for n-body simulation.

This module provides 3D plotting and animation capabilities for visualizing
gravitational n-body simulations.
"""

from .plotter3d import Plotter3D, create_static_plot, quick_plot
from .animation import (
    InteractiveAnimation,
    SimpleAnimation,
    create_interactive_animation,
    create_simple_animation
)

__all__ = [
    'Plotter3D',
    'create_static_plot',
    'quick_plot',
    'InteractiveAnimation',
    'SimpleAnimation',
    'create_interactive_animation',
    'create_simple_animation'
]