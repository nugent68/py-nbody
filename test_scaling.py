#!/usr/bin/env python3
"""
Test script to verify the visualization scaling is working correctly.
"""
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.physics import PhysicsEngine
from src.config import get_preset_system
from src.visualization import create_static_plot

def test_visualization_scaling():
    """Test that visualization scaling works correctly for astronomical distances."""
    print("Testing visualization scaling...")
    
    # Create engine with inner solar system
    engine = PhysicsEngine(integration_method="rk4")
    engine.set_time_step(86400.0 * 10)  # 10 days per step
    
    bodies = get_preset_system("inner")
    engine.add_bodies(bodies)
    
    print(f"Created {len(bodies)} bodies:")
    AU = 1.496e11  # meters
    
    for body in bodies:
        x_au = body.position.x / AU
        y_au = body.position.y / AU
        z_au = body.position.z / AU
        print(f"  {body.name}: ({x_au:.3f}, {y_au:.3f}, {z_au:.3f}) AU")
    
    # Run simulation to generate some trajectory data
    print("\nRunning simulation for 20 steps to generate trajectories...")
    engine.run(steps=20)
    
    # Test the plotter scaling
    print("\nTesting plotter scaling...")
    plotter = create_static_plot(engine.bodies, engine, show_trails=True)
    
    # Get the axis limits to verify they're in reasonable AU ranges
    xlim = plotter.ax.get_xlim()
    ylim = plotter.ax.get_ylim()
    zlim = plotter.ax.get_zlim()
    
    print(f"Plot limits:")
    print(f"  X: {xlim[0]:.2f} to {xlim[1]:.2f} AU")
    print(f"  Y: {ylim[0]:.2f} to {ylim[1]:.2f} AU")
    print(f"  Z: {zlim[0]:.2f} to {zlim[1]:.2f} AU")
    
    # Verify the limits are reasonable (should be on the order of a few AU)
    x_range = xlim[1] - xlim[0]
    y_range = ylim[1] - ylim[0]
    z_range = zlim[1] - zlim[0]
    
    print(f"\nPlot ranges:")
    print(f"  X range: {x_range:.2f} AU")
    print(f"  Y range: {y_range:.2f} AU")
    print(f"  Z range: {z_range:.2f} AU")
    
    # Check that the ranges are reasonable (should be a few AU for inner solar system)
    if 1 <= x_range <= 10 and 1 <= y_range <= 10 and 1 <= z_range <= 10:
        print("✅ Scaling looks correct - ranges are in reasonable AU scale")
        return True
    else:
        print("❌ Scaling may be incorrect - ranges seem too large or small")
        return False

def test_earth_moon_scaling():
    """Test scaling for Earth-Moon system (much smaller scale)."""
    print("\n" + "="*50)
    print("Testing Earth-Moon system scaling...")
    
    # Create Earth-Moon system
    engine = PhysicsEngine(integration_method="rk4")
    engine.set_time_step(3600.0)  # 1 hour per step
    
    bodies = get_preset_system("earth_moon")
    engine.add_bodies(bodies)
    
    AU = 1.496e11  # meters
    
    print(f"Created {len(bodies)} bodies:")
    for body in bodies:
        x_au = body.position.x / AU
        y_au = body.position.y / AU
        z_au = body.position.z / AU
        print(f"  {body.name}: ({x_au:.6f}, {y_au:.6f}, {z_au:.6f}) AU")
    
    # Run simulation
    engine.run(steps=10)
    
    # Test the plotter scaling
    plotter = create_static_plot(engine.bodies, engine, show_trails=True)
    
    xlim = plotter.ax.get_xlim()
    ylim = plotter.ax.get_ylim()
    zlim = plotter.ax.get_zlim()
    
    print(f"\nPlot limits:")
    print(f"  X: {xlim[0]:.4f} to {xlim[1]:.4f} AU")
    print(f"  Y: {ylim[0]:.4f} to {ylim[1]:.4f} AU")
    print(f"  Z: {zlim[0]:.4f} to {zlim[1]:.4f} AU")
    
    # For Earth-Moon, the range should be very small (Moon is ~0.00257 AU from Earth)
    x_range = xlim[1] - xlim[0]
    
    if 0.001 <= x_range <= 0.1:  # Should be small fraction of AU
        print("✅ Earth-Moon scaling looks correct")
        return True
    else:
        print("❌ Earth-Moon scaling may be incorrect")
        return False

def main():
    """Run scaling tests."""
    print("=" * 60)
    print("Visualization Scaling Test Suite")
    print("=" * 60)
    
    try:
        # Test inner solar system scaling
        result1 = test_visualization_scaling()
        
        # Test Earth-Moon scaling
        result2 = test_earth_moon_scaling()
        
        print("\n" + "=" * 60)
        if result1 and result2:
            print("✅ ALL SCALING TESTS PASSED!")
            print("The visualization should now display planets at proper scales.")
            print("Axes are labeled in AU (Astronomical Units) for better readability.")
        else:
            print("❌ SOME SCALING TESTS FAILED!")
        print("=" * 60)
        
        return result1 and result2
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)