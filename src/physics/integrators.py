"""
Numerical integration methods for n-body simulation.
"""
from typing import List, Callable
from .body import Body
from .vector3d import Vector3D


class Integrator:
    """Base class for numerical integrators."""
    
    def __init__(self, name: str):
        self.name = name
    
    def step(self, bodies: List[Body], dt: float, force_calculator: Callable) -> None:
        """
        Perform one integration step.
        
        Args:
            bodies: List of Body objects
            dt: Time step
            force_calculator: Function that calculates forces on all bodies
        """
        raise NotImplementedError("Subclasses must implement step method")


class EulerIntegrator(Integrator):
    """
    Simple Euler integration method.
    Fast but less accurate, suitable for educational purposes.
    """
    
    def __init__(self):
        super().__init__("Euler")
    
    def step(self, bodies: List[Body], dt: float, force_calculator: Callable) -> None:
        """
        Perform one Euler integration step.
        
        The Euler method updates positions and velocities using:
        v(t+dt) = v(t) + a(t) * dt
        r(t+dt) = r(t) + v(t) * dt
        
        Args:
            bodies: List of Body objects
            dt: Time step
            force_calculator: Function that calculates forces on all bodies
        """
        # Calculate forces and accelerations at current time
        force_calculator(bodies)
        
        # Update velocities first (using current accelerations)
        for body in bodies:
            body.update_velocity(dt)
        
        # Update positions (using updated velocities)
        for body in bodies:
            body.update_position(dt)


class RK4Integrator(Integrator):
    """
    4th-order Runge-Kutta integration method.
    More accurate but computationally more expensive.
    """
    
    def __init__(self):
        super().__init__("RK4")
    
    def step(self, bodies: List[Body], dt: float, force_calculator: Callable) -> None:
        """
        Perform one RK4 integration step.
        
        The RK4 method uses four evaluations of the derivative to achieve
        4th-order accuracy in the time step.
        
        Args:
            bodies: List of Body objects
            dt: Time step
            force_calculator: Function that calculates forces on all bodies
        """
        n = len(bodies)
        
        # Store initial state
        initial_positions = [Vector3D(body.position.x, body.position.y, body.position.z) 
                           for body in bodies]
        initial_velocities = [Vector3D(body.velocity.x, body.velocity.y, body.velocity.z) 
                            for body in bodies]
        
        # Arrays to store k values for position and velocity
        k1_pos = [Vector3D() for _ in range(n)]
        k1_vel = [Vector3D() for _ in range(n)]
        k2_pos = [Vector3D() for _ in range(n)]
        k2_vel = [Vector3D() for _ in range(n)]
        k3_pos = [Vector3D() for _ in range(n)]
        k3_vel = [Vector3D() for _ in range(n)]
        k4_pos = [Vector3D() for _ in range(n)]
        k4_vel = [Vector3D() for _ in range(n)]
        
        # k1: derivatives at t
        force_calculator(bodies)
        for i, body in enumerate(bodies):
            k1_pos[i] = body.velocity * dt
            k1_vel[i] = body.acceleration * dt
        
        # k2: derivatives at t + dt/2 using k1
        for i, body in enumerate(bodies):
            body.position = initial_positions[i] + k1_pos[i] * 0.5
            body.velocity = initial_velocities[i] + k1_vel[i] * 0.5
        
        force_calculator(bodies)
        for i, body in enumerate(bodies):
            k2_pos[i] = body.velocity * dt
            k2_vel[i] = body.acceleration * dt
        
        # k3: derivatives at t + dt/2 using k2
        for i, body in enumerate(bodies):
            body.position = initial_positions[i] + k2_pos[i] * 0.5
            body.velocity = initial_velocities[i] + k2_vel[i] * 0.5
        
        force_calculator(bodies)
        for i, body in enumerate(bodies):
            k3_pos[i] = body.velocity * dt
            k3_vel[i] = body.acceleration * dt
        
        # k4: derivatives at t + dt using k3
        for i, body in enumerate(bodies):
            body.position = initial_positions[i] + k3_pos[i]
            body.velocity = initial_velocities[i] + k3_vel[i]
        
        force_calculator(bodies)
        for i, body in enumerate(bodies):
            k4_pos[i] = body.velocity * dt
            k4_vel[i] = body.acceleration * dt
        
        # Final update using weighted average of k values
        for i, body in enumerate(bodies):
            # RK4 formula: y(t+dt) = y(t) + (k1 + 2*k2 + 2*k3 + k4)/6
            pos_increment = (k1_pos[i] + k2_pos[i] * 2 + k3_pos[i] * 2 + k4_pos[i]) / 6
            vel_increment = (k1_vel[i] + k2_vel[i] * 2 + k3_vel[i] * 2 + k4_vel[i]) / 6
            
            body.position = initial_positions[i] + pos_increment
            body.velocity = initial_velocities[i] + vel_increment
            
            # Update trajectory
            body.trajectory.append(Vector3D(body.position.x, body.position.y, body.position.z))


class LeapfrogIntegrator(Integrator):
    """
    Leapfrog integration method.
    Symplectic integrator that conserves energy well for orbital mechanics.
    """
    
    def __init__(self):
        super().__init__("Leapfrog")
        self.first_step = True
    
    def step(self, bodies: List[Body], dt: float, force_calculator: Callable) -> None:
        """
        Perform one leapfrog integration step.
        
        The leapfrog method staggers position and velocity updates:
        v(t+dt/2) = v(t-dt/2) + a(t) * dt
        r(t+dt) = r(t) + v(t+dt/2) * dt
        
        Args:
            bodies: List of Body objects
            dt: Time step
            force_calculator: Function that calculates forces on all bodies
        """
        if self.first_step:
            # For the first step, use Euler to get v(t+dt/2)
            force_calculator(bodies)
            for body in bodies:
                body.velocity = body.velocity + body.acceleration * (dt / 2)
            self.first_step = False
        
        # Calculate forces at current positions
        force_calculator(bodies)
        
        # Update velocities by full step
        for body in bodies:
            body.velocity = body.velocity + body.acceleration * dt
        
        # Update positions using new velocities
        for body in bodies:
            body.update_position(dt)


def get_integrator(method: str) -> Integrator:
    """
    Factory function to get integrator by name.
    
    Args:
        method: Integration method name ('euler', 'rk4', 'leapfrog')
        
    Returns:
        Integrator instance
        
    Raises:
        ValueError: If method is not recognized
    """
    method = method.lower()
    
    if method == 'euler':
        return EulerIntegrator()
    elif method == 'rk4':
        return RK4Integrator()
    elif method == 'leapfrog':
        return LeapfrogIntegrator()
    else:
        raise ValueError(f"Unknown integration method: {method}. "
                        f"Available methods: 'euler', 'rk4', 'leapfrog'")