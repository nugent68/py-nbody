"""
Simple demonstration of the n-body simulation.

This script shows how to create and run a basic solar system simulation
with the py-nbody package.
"""
import sys
from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt

# Ensure we use an interactive backend for GUI display
try:
    # Try to use a GUI backend
    matplotlib.use('TkAgg')  # or 'Qt5Agg' if available
except ImportError:
    try:
        matplotlib.use('Qt5Agg')
    except ImportError:
        print("Warning: No GUI backend available. Using default backend.")
        pass

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.physics import PhysicsEngine, Body, Vector3D
from src.config import get_preset_system
from src.visualization import quick_plot, create_interactive_animation


def demo_earth_moon_system():
    """Demonstrate Earth-Moon system simulation."""
    print("Creating Earth-Moon system...")
    
    # Create physics engine
    engine = PhysicsEngine(integration_method="rk4")
    engine.set_time_step(3600.0)  # 1 hour time steps
    
    # Get Earth-Moon system
    bodies = get_preset_system("earth_moon")
    engine.add_bodies(bodies)
    
    print(f"System created with {len(bodies)} bodies:")
    for body in bodies:
        print(f"  - {body.name}: mass={body.mass:.2e} kg")
    
    # Run simulation for 30 days
    print("Running simulation for 30 days...")
    steps = 24 * 30  # 30 days * 24 hours
    engine.run(steps=steps)
    
    # Show results
    print("Displaying results...")
    try:
        quick_plot(engine.bodies, show_trails=True)
        plt.show(block=True)  # Keep window open until user closes it
    except Exception as e:
        print(f"Error displaying plot: {e}")


def demo_inner_solar_system():
    """Demonstrate inner solar system simulation."""
    print("Creating inner solar system...")
    
    # Create physics engine
    engine = PhysicsEngine(integration_method="rk4")
    engine.set_time_step(86400.0 * 5)  # 5 days per step
    
    # Get inner solar system
    bodies = get_preset_system("inner")
    engine.add_bodies(bodies)
    
    print(f"System created with {len(bodies)} bodies:")
    for body in bodies:
        print(f"  - {body.name}: mass={body.mass:.2e} kg")
    
    # Run simulation for 2 years
    print("Running simulation for 2 years...")
    steps = int(365.25 * 2 / 5)  # 2 years / 5 days per step
    engine.run(steps=steps)
    
    # Analyze energy conservation
    analysis = engine.get_conservation_analysis()
    print(f"\nEnergy conservation analysis:")
    print(f"  Initial energy: {analysis['energy']['initial']:.2e} J")
    print(f"  Final energy: {analysis['energy']['final']:.2e} J")
    print(f"  Energy drift: {analysis['energy']['drift_percent']:.6f}%")
    
    # Show results
    print("Displaying results...")
    try:
        quick_plot(engine.bodies, show_trails=True)
        plt.show(block=True)  # Keep window open until user closes it
    except Exception as e:
        print(f"Error displaying plot: {e}")


def demo_custom_system():
    """Demonstrate custom two-body system."""
    print("Creating custom two-body system...")
    
    # Create custom bodies
    star = Body(
        mass=1.989e30,  # Solar mass
        position=Vector3D(0, 0, 0),
        velocity=Vector3D(0, 0, 0),
        name="Star",
        color="yellow"
    )
    
    planet = Body(
        mass=5.972e24,  # Earth mass
        position=Vector3D(1.496e11, 0, 0),  # 1 AU
        velocity=Vector3D(0, 29780, 0),  # Earth orbital velocity
        name="Planet",
        color="blue"
    )
    
    # Create physics engine
    engine = PhysicsEngine(integration_method="rk4")
    engine.set_time_step(86400.0)  # 1 day
    engine.add_bodies([star, planet])
    
    print(f"System created with {len(engine.bodies)} bodies:")
    for body in engine.bodies:
        print(f"  - {body.name}: mass={body.mass:.2e} kg")
    
    # Run simulation for 1 year
    print("Running simulation for 1 year...")
    engine.run(steps=365)
    
    # Calculate orbital period
    # Find when planet completes one orbit (returns close to starting position)
    initial_pos = Vector3D(1.496e11, 0, 0)
    min_distance = float('inf')
    closest_step = 0
    
    for i, pos in enumerate(planet.trajectory[100:], 100):  # Skip first 100 steps
        distance = pos.distance_to(initial_pos)
        if distance < min_distance:
            min_distance = distance
            closest_step = i
    
    orbital_period_days = closest_step
    print(f"\nOrbital analysis:")
    print(f"  Simulated orbital period: {orbital_period_days} days")
    print(f"  Expected orbital period: 365.25 days")
    print(f"  Error: {abs(orbital_period_days - 365.25):.1f} days")
    
    # Show results
    print("Displaying results...")
    try:
        quick_plot(engine.bodies, show_trails=True)
        plt.show(block=True)  # Keep window open until user closes it
    except Exception as e:
        print(f"Error displaying plot: {e}")


def demo_interactive():
    """Demonstrate interactive simulation."""
    print("Creating interactive simulation...")
    print("This will open an interactive window with controls.")
    print("Use the Play/Pause button to control the simulation.")
    print("Close the window when you're done to continue.")
    
    # Create physics engine
    engine = PhysicsEngine(integration_method="rk4")
    engine.set_time_step(86400.0 * 2)  # 2 days per step
    
    # Get inner solar system
    bodies = get_preset_system("inner")
    engine.add_bodies(bodies)
    
    print(f"System created with {len(bodies)} bodies:")
    for body in bodies:
        print(f"  - {body.name}: mass={body.mass:.2e} kg")
    
    # Create interactive animation
    try:
        animation = create_interactive_animation(engine, update_interval=100)
        
        # Show the animation and keep it alive
        print("Opening interactive window...")
        animation.show()
        
        # Keep the script running until the window is closed
        plt.show(block=True)
        
    except Exception as e:
        print(f"Error creating interactive animation: {e}")
        print("Falling back to static plot...")
        # Run a short simulation and show static plot
        engine.run(steps=50)
        quick_plot(engine.bodies, show_trails=True)


def main():
    """Main demonstration function."""
    print("N-Body Simulation Demonstrations")
    print("=" * 40)
    
    demos = {
        "1": ("Earth-Moon System", demo_earth_moon_system),
        "2": ("Inner Solar System", demo_inner_solar_system),
        "3": ("Custom Two-Body System", demo_custom_system),
        "4": ("Interactive Simulation", demo_interactive),
    }
    
    print("\nAvailable demonstrations:")
    for key, (name, _) in demos.items():
        print(f"  {key}. {name}")
    
    try:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice in demos:
            name, demo_func = demos[choice]
            print(f"\nRunning: {name}")
            print("-" * 40)
            demo_func()
        else:
            print("Invalid choice. Running Earth-Moon demo by default.")
            demo_earth_moon_system()
            
    except KeyboardInterrupt:
        print("\nDemo interrupted by user.")
    except Exception as e:
        print(f"Error running demo: {e}")


if __name__ == "__main__":
    main()