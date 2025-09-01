"""
Main physics engine for n-body simulation.
"""
import time
from typing import List, Optional, Dict, Any
from .body import Body
from .vector3d import Vector3D
from .integrators import get_integrator, Integrator
from .forces import GravitationalForceCalculator, create_force_calculator


class PhysicsEngine:
    """
    Main physics engine that orchestrates the n-body simulation.
    """
    
    def __init__(self, 
                 integration_method: str = "rk4",
                 force_method: str = "standard",
                 **force_kwargs):
        """
        Initialize the physics engine.
        
        Args:
            integration_method: Integration method ('euler', 'rk4', 'leapfrog')
            force_method: Force calculation method ('standard', 'softened')
            **force_kwargs: Additional arguments for force calculator
        """
        self.integrator = get_integrator(integration_method)
        self.force_calculator = create_force_calculator(force_method, **force_kwargs)
        
        self.bodies = []
        self.time = 0.0
        self.step_count = 0
        
        # Simulation parameters
        self.dt = 1.0  # Default time step (seconds)
        self.max_steps = None
        self.max_time = None
        
        # Performance tracking
        self.simulation_start_time = None
        self.last_step_time = None
        
        # Energy and momentum tracking for validation
        self.energy_history = []
        self.momentum_history = []
        self.angular_momentum_history = []
        
    def add_body(self, body: Body) -> None:
        """
        Add a body to the simulation.
        
        Args:
            body: Body object to add
        """
        self.bodies.append(body)
    
    def add_bodies(self, bodies: List[Body]) -> None:
        """
        Add multiple bodies to the simulation.
        
        Args:
            bodies: List of Body objects to add
        """
        self.bodies.extend(bodies)
    
    def remove_body(self, body: Body) -> None:
        """
        Remove a body from the simulation.
        
        Args:
            body: Body object to remove
        """
        if body in self.bodies:
            self.bodies.remove(body)
    
    def clear_bodies(self) -> None:
        """Remove all bodies from the simulation."""
        self.bodies.clear()
    
    def set_time_step(self, dt: float) -> None:
        """
        Set the simulation time step.
        
        Args:
            dt: Time step in seconds
        """
        self.dt = dt
    
    def reset_simulation(self) -> None:
        """Reset simulation time and step count."""
        self.time = 0.0
        self.step_count = 0
        self.energy_history.clear()
        self.momentum_history.clear()
        self.angular_momentum_history.clear()
        
        # Clear trajectories
        for body in self.bodies:
            body.clear_trajectory()
    
    def step(self) -> None:
        """Perform one simulation step."""
        if not self.bodies:
            return
        
        step_start_time = time.time()
        
        # Perform integration step
        self.integrator.step(self.bodies, self.dt, self.force_calculator.calculate_forces)
        
        # Update simulation state
        self.time += self.dt
        self.step_count += 1
        
        # Track performance
        self.last_step_time = time.time() - step_start_time
        
        # Record conservation quantities for validation
        self._record_conservation_quantities()
    
    def run(self, 
            steps: Optional[int] = None, 
            duration: Optional[float] = None,
            callback: Optional[callable] = None,
            callback_interval: int = 1) -> None:
        """
        Run the simulation for a specified number of steps or duration.
        
        Args:
            steps: Number of steps to run (takes precedence over duration)
            duration: Duration to run in simulation time (seconds)
            callback: Optional callback function called every callback_interval steps
            callback_interval: How often to call the callback (in steps)
        """
        if steps is None and duration is None:
            raise ValueError("Must specify either steps or duration")
        
        self.simulation_start_time = time.time()
        
        if steps is not None:
            target_steps = self.step_count + steps
            while self.step_count < target_steps:
                self.step()
                
                if callback and self.step_count % callback_interval == 0:
                    callback(self)
        
        elif duration is not None:
            target_time = self.time + duration
            while self.time < target_time:
                self.step()
                
                if callback and self.step_count % callback_interval == 0:
                    callback(self)
    
    def get_system_energy(self) -> tuple:
        """
        Get current system energy.
        
        Returns:
            Tuple of (kinetic_energy, potential_energy, total_energy)
        """
        return self.force_calculator.calculate_total_energy(self.bodies)
    
    def get_center_of_mass(self) -> Vector3D:
        """Get current center of mass."""
        return self.force_calculator.calculate_center_of_mass(self.bodies)
    
    def get_total_momentum(self) -> Vector3D:
        """Get current total momentum."""
        return self.force_calculator.calculate_total_momentum(self.bodies)
    
    def get_total_angular_momentum(self, origin: Vector3D = None) -> Vector3D:
        """Get current total angular momentum."""
        return self.force_calculator.calculate_total_angular_momentum(self.bodies, origin)
    
    def _record_conservation_quantities(self) -> None:
        """Record energy and momentum for conservation analysis."""
        kinetic, potential, total = self.get_system_energy()
        momentum = self.get_total_momentum()
        angular_momentum = self.get_total_angular_momentum()
        
        self.energy_history.append({
            'time': self.time,
            'kinetic': kinetic,
            'potential': potential,
            'total': total
        })
        
        self.momentum_history.append({
            'time': self.time,
            'momentum': momentum
        })
        
        self.angular_momentum_history.append({
            'time': self.time,
            'angular_momentum': angular_momentum
        })
    
    def get_conservation_analysis(self) -> Dict[str, Any]:
        """
        Analyze conservation of energy and momentum.
        
        Returns:
            Dictionary with conservation analysis results
        """
        if len(self.energy_history) < 2:
            return {"error": "Not enough data for analysis"}
        
        # Energy conservation analysis
        initial_energy = self.energy_history[0]['total']
        final_energy = self.energy_history[-1]['total']
        energy_drift = abs(final_energy - initial_energy)
        energy_drift_percent = (energy_drift / abs(initial_energy)) * 100 if initial_energy != 0 else 0
        
        # Momentum conservation analysis
        initial_momentum = self.momentum_history[0]['momentum']
        final_momentum = self.momentum_history[-1]['momentum']
        momentum_drift = (final_momentum - initial_momentum).magnitude()
        
        # Angular momentum conservation analysis
        initial_angular_momentum = self.angular_momentum_history[0]['angular_momentum']
        final_angular_momentum = self.angular_momentum_history[-1]['angular_momentum']
        angular_momentum_drift = (final_angular_momentum - initial_angular_momentum).magnitude()
        
        return {
            'energy': {
                'initial': initial_energy,
                'final': final_energy,
                'drift': energy_drift,
                'drift_percent': energy_drift_percent
            },
            'momentum': {
                'initial_magnitude': initial_momentum.magnitude(),
                'final_magnitude': final_momentum.magnitude(),
                'drift': momentum_drift
            },
            'angular_momentum': {
                'initial_magnitude': initial_angular_momentum.magnitude(),
                'final_magnitude': final_angular_momentum.magnitude(),
                'drift': angular_momentum_drift
            },
            'simulation_info': {
                'time': self.time,
                'steps': self.step_count,
                'dt': self.dt,
                'integrator': self.integrator.name
            }
        }
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """
        Get performance statistics.
        
        Returns:
            Dictionary with performance information
        """
        if self.simulation_start_time is None:
            return {"error": "Simulation not started"}
        
        total_time = time.time() - self.simulation_start_time
        steps_per_second = self.step_count / total_time if total_time > 0 else 0
        
        return {
            'total_simulation_time': total_time,
            'steps_completed': self.step_count,
            'steps_per_second': steps_per_second,
            'last_step_time': self.last_step_time,
            'simulation_time': self.time,
            'time_step': self.dt
        }
    
    def __str__(self) -> str:
        """String representation."""
        return (f"PhysicsEngine(bodies={len(self.bodies)}, "
                f"time={self.time:.2f}, steps={self.step_count}, "
                f"integrator={self.integrator.name})")