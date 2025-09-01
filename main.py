"""
Main application for n-body gravitational simulation.

This is the entry point for running the 3D n-body simulation with
interactive visualization and controls.
"""
import argparse
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.physics import PhysicsEngine
from src.config import get_preset_system, SimulationParameters
from src.visualization import create_interactive_animation, create_static_plot, quick_plot


def create_simulation(preset: str = "inner", 
                     integration_method: str = "rk4",
                     time_step: float = 86400.0,
                     scale_factor: float = 1.0,
                     time_scale: float = 1.0) -> PhysicsEngine:
    """
    Create and configure a simulation.
    
    Args:
        preset: System preset ('inner', 'full', 'earth_moon')
        integration_method: Integration method ('euler', 'rk4', 'leapfrog')
        time_step: Time step in seconds
        scale_factor: Distance scale factor
        time_scale: Time scale factor
        
    Returns:
        Configured PhysicsEngine instance
    """
    # Create physics engine
    engine = PhysicsEngine(integration_method=integration_method)
    engine.set_time_step(time_step)
    
    # Create system bodies
    bodies = get_preset_system(preset, scale_factor=scale_factor, time_scale=time_scale)
    engine.add_bodies(bodies)
    
    return engine


def run_interactive_simulation(engine: PhysicsEngine) -> None:
    """
    Run interactive simulation with controls.
    
    Args:
        engine: PhysicsEngine instance
    """
    print("Starting interactive n-body simulation...")
    print("Controls:")
    print("  - Play/Pause: Toggle simulation")
    print("  - Reset: Reset to initial conditions")
    print("  - Speed slider: Adjust simulation speed")
    print("  - Trail slider: Adjust orbital trail length")
    print("  - Mouse: Rotate and zoom the 3D view")
    
    # Create interactive animation
    animation = create_interactive_animation(engine, update_interval=50)
    
    # Show the animation
    animation.show()


def run_static_plot(engine: PhysicsEngine, steps: int = 1000) -> None:
    """
    Run simulation and show static plot.
    
    Args:
        engine: PhysicsEngine instance
        steps: Number of simulation steps to run
    """
    print(f"Running simulation for {steps} steps...")
    
    # Run simulation
    engine.run(steps=steps)
    
    # Create and show static plot
    plotter = create_static_plot(engine.bodies, engine, show_trails=True)
    plotter.show()


def run_quick_demo() -> None:
    """Run a quick demonstration of the simulation."""
    print("Running quick demo of inner solar system...")
    
    # Create simple simulation
    engine = create_simulation(preset="inner", time_step=86400.0 * 10)  # 10 days per step
    
    # Run for a short time to generate some orbits
    engine.run(steps=100)
    
    # Show quick plot
    quick_plot(engine.bodies, show_trails=True)


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(description="3D N-Body Gravitational Simulation")
    
    parser.add_argument("--preset", choices=["inner", "full", "earth_moon"], 
                       default="inner", help="Solar system preset")
    parser.add_argument("--integrator", choices=["euler", "rk4", "leapfrog"],
                       default="rk4", help="Integration method")
    parser.add_argument("--time-step", type=float, default=86400.0,
                       help="Time step in seconds (default: 1 day)")
    parser.add_argument("--scale-factor", type=float, default=1.0,
                       help="Distance scale factor")
    parser.add_argument("--time-scale", type=float, default=1.0,
                       help="Time scale factor")
    parser.add_argument("--mode", choices=["interactive", "static", "demo"],
                       default="interactive", help="Simulation mode")
    parser.add_argument("--steps", type=int, default=1000,
                       help="Number of steps for static mode")
    parser.add_argument("--config", type=str, help="Configuration file path")
    
    args = parser.parse_args()
    
    try:
        if args.mode == "demo":
            run_quick_demo()
            return
        
        # Load configuration if provided
        if args.config:
            params = SimulationParameters(args.config)
            params.validate()
            
            # Use config parameters
            preset = params.get('system.preset', args.preset)
            integrator = params.get('simulation.integration_method', args.integrator)
            time_step = params.get('simulation.time_step', args.time_step)
            scale_factor = params.get('system.scale_factor', args.scale_factor)
            time_scale = params.get('system.time_scale', args.time_scale)
        else:
            # Use command line arguments
            preset = args.preset
            integrator = args.integrator
            time_step = args.time_step
            scale_factor = args.scale_factor
            time_scale = args.time_scale
        
        # Create simulation
        engine = create_simulation(
            preset=preset,
            integration_method=integrator,
            time_step=time_step,
            scale_factor=scale_factor,
            time_scale=time_scale
        )
        
        print(f"Created {preset} solar system simulation")
        print(f"Integration method: {integrator}")
        print(f"Time step: {time_step:.2e} seconds")
        print(f"Number of bodies: {len(engine.bodies)}")
        
        # Run simulation based on mode
        if args.mode == "interactive":
            run_interactive_simulation(engine)
        elif args.mode == "static":
            run_static_plot(engine, args.steps)
        
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()