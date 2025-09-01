"""
Headless version of the main application for n-body gravitational simulation.

This version is designed to work in environments without GUI display,
automatically saving visualization images instead of showing interactive windows.
"""
import argparse
import sys
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.physics import PhysicsEngine
from src.config import get_preset_system, SimulationParameters
from src.visualization import create_static_plot, quick_plot


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


def run_headless_simulation(engine: PhysicsEngine, steps: int = 100, 
                           save_interval: int = 20, output_dir: str = "output") -> None:
    """
    Run simulation in headless mode, saving images at intervals.
    
    Args:
        engine: PhysicsEngine instance
        steps: Number of simulation steps to run
        save_interval: How often to save images (in steps)
        output_dir: Directory to save images
    """
    print(f"Running headless simulation for {steps} steps...")
    print(f"Saving images every {save_interval} steps to '{output_dir}/' directory")
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    # Save initial state
    plotter = create_static_plot(engine.bodies, engine, show_trails=True)
    initial_file = f"{output_dir}/step_000_initial.png"
    plotter.save_plot(initial_file, dpi=150)
    print(f"Saved initial state: {initial_file}")
    plt.close(plotter.fig)
    
    # Run simulation with periodic saves
    for step in range(1, steps + 1):
        engine.step()
        
        if step % save_interval == 0 or step == steps:
            # Create and save plot
            plotter = create_static_plot(engine.bodies, engine, show_trails=True)
            filename = f"{output_dir}/step_{step:03d}.png"
            plotter.save_plot(filename, dpi=150)
            
            # Get system info
            kinetic, potential, total = engine.get_system_energy()
            print(f"Step {step:3d}: Time={engine.time:.2e}s, Energy={total:.2e}J, Saved: {filename}")
            plt.close(plotter.fig)
    
    print(f"\nSimulation complete! Check the '{output_dir}/' directory for visualization images.")


def run_static_plot(engine: PhysicsEngine, steps: int = 1000, output_file: str = None) -> None:
    """
    Run simulation and save static plot.
    
    Args:
        engine: PhysicsEngine instance
        steps: Number of simulation steps to run
        output_file: Output filename (default: auto-generated)
    """
    print(f"Running simulation for {steps} steps...")
    
    # Run simulation
    engine.run(steps=steps)
    
    # Create and save static plot
    plotter = create_static_plot(engine.bodies, engine, show_trails=True)
    
    if output_file is None:
        output_file = f"simulation_{engine.integrator.name}_{steps}steps.png"
    
    plotter.save_plot(output_file, dpi=200)
    print(f"Simulation complete! Saved visualization: {output_file}")
    plt.close(plotter.fig)


def run_quick_demo(output_file: str = "demo_output.png") -> None:
    """Run a quick demonstration of the simulation."""
    print("Running quick demo of inner solar system...")
    
    # Create simple simulation
    engine = create_simulation(preset="inner", time_step=86400.0 * 5)  # 5 days per step
    
    # Run for a short time to generate some orbits
    engine.run(steps=50)
    
    # Save plot
    plotter = create_static_plot(engine.bodies, engine, show_trails=True)
    plotter.save_plot(output_file, dpi=150)
    print(f"Demo complete! Saved visualization: {output_file}")
    plt.close(plotter.fig)


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(description="3D N-Body Gravitational Simulation (Headless Mode)")
    
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
    parser.add_argument("--mode", choices=["animated", "static", "demo"],
                       default="animated", help="Simulation mode")
    parser.add_argument("--steps", type=int, default=100,
                       help="Number of steps to run")
    parser.add_argument("--save-interval", type=int, default=20,
                       help="Save image every N steps (for animated mode)")
    parser.add_argument("--output", type=str, help="Output filename or directory")
    parser.add_argument("--config", type=str, help="Configuration file path")
    
    args = parser.parse_args()
    
    try:
        if args.mode == "demo":
            output_file = args.output or "demo_output.png"
            run_quick_demo(output_file)
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
        if args.mode == "animated":
            output_dir = args.output or f"animation_{preset}_{integrator}"
            run_headless_simulation(engine, args.steps, args.save_interval, output_dir)
        elif args.mode == "static":
            output_file = args.output or f"{preset}_{integrator}_{args.steps}steps.png"
            run_static_plot(engine, args.steps, output_file)
        
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()