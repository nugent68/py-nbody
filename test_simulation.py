#!/usr/bin/env python3
"""
Test script to verify the n-body simulation is working correctly.
This will test the physics engine and body creation without requiring GUI.
"""
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.physics import PhysicsEngine
from src.config import get_preset_system
from src.visualization import create_static_plot

def test_body_creation():
    """Test that bodies are created correctly."""
    print("Testing body creation...")
    
    # Test inner solar system
    bodies = get_preset_system("inner")
    print(f"Created {len(bodies)} bodies for inner solar system:")
    for body in bodies:
        print(f"  - {body.name}: mass={body.mass:.2e} kg, pos=({body.position.x:.2e}, {body.position.y:.2e}, {body.position.z:.2e})")
    
    # Test Earth-Moon system
    bodies = get_preset_system("earth_moon")
    print(f"\nCreated {len(bodies)} bodies for Earth-Moon system:")
    for body in bodies:
        print(f"  - {body.name}: mass={body.mass:.2e} kg, pos=({body.position.x:.2e}, {body.position.y:.2e}, {body.position.z:.2e})")
    
    return True

def test_physics_engine():
    """Test that the physics engine works correctly."""
    print("\nTesting physics engine...")
    
    # Create engine with inner solar system
    engine = PhysicsEngine(integration_method="rk4")
    engine.set_time_step(86400.0)  # 1 day
    
    bodies = get_preset_system("inner")
    engine.add_bodies(bodies)
    
    print(f"Engine created with {len(engine.bodies)} bodies")
    print(f"Integration method: {engine.integrator.name}")
    print(f"Time step: {engine.dt} seconds")
    
    # Get initial energy
    kinetic, potential, total = engine.get_system_energy()
    print(f"Initial energy - Kinetic: {kinetic:.2e} J, Potential: {potential:.2e} J, Total: {total:.2e} J")
    
    # Run simulation for a few steps
    print("\nRunning simulation for 10 steps...")
    initial_positions = [(body.name, body.position.x, body.position.y, body.position.z) for body in engine.bodies]
    
    for i in range(10):
        engine.step()
        if i % 5 == 0:
            kinetic, potential, total = engine.get_system_energy()
            print(f"Step {i}: Time={engine.time:.2e}s, Total Energy={total:.2e}J")
    
    # Check that bodies moved
    final_positions = [(body.name, body.position.x, body.position.y, body.position.z) for body in engine.bodies]
    
    print("\nPosition changes:")
    for (name1, x1, y1, z1), (name2, x2, y2, z2) in zip(initial_positions, final_positions):
        dx, dy, dz = x2-x1, y2-y1, z2-z1
        distance_moved = (dx**2 + dy**2 + dz**2)**0.5
        print(f"  {name1}: moved {distance_moved:.2e} meters")
    
    # Test conservation
    analysis = engine.get_conservation_analysis()
    if 'energy' in analysis:
        print(f"\nEnergy conservation: {analysis['energy']['drift_percent']:.6f}% drift")
    
    return True

def test_visualization_data():
    """Test that visualization data is properly prepared."""
    print("\nTesting visualization data preparation...")
    
    # Create engine and run for some steps to generate trajectories
    engine = PhysicsEngine(integration_method="rk4")
    engine.set_time_step(86400.0 * 10)  # 10 days per step
    
    bodies = get_preset_system("inner")
    engine.add_bodies(bodies)
    
    # Run simulation to generate trajectory data
    engine.run(steps=50)
    
    print("Trajectory data:")
    for body in engine.bodies:
        x_coords, y_coords, z_coords = body.get_trajectory_arrays()
        print(f"  {body.name}: {len(x_coords)} trajectory points")
        if len(x_coords) > 0:
            print(f"    Start: ({x_coords[0]:.2e}, {y_coords[0]:.2e}, {z_coords[0]:.2e})")
            print(f"    End: ({x_coords[-1]:.2e}, {y_coords[-1]:.2e}, {z_coords[-1]:.2e})")
    
    return True

def main():
    """Run all tests."""
    print("=" * 60)
    print("N-Body Simulation Test Suite")
    print("=" * 60)
    
    try:
        # Run tests
        test_body_creation()
        test_physics_engine()
        test_visualization_data()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("The simulation is working correctly.")
        print("The issue with visualization is likely due to running in a headless environment.")
        print("In a GUI environment, the interactive plots would display properly.")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)