#!/usr/bin/env python3
"""
Test script to verify the interactive animation fix works correctly.
"""
import sys
from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt

# Use GUI backend for testing
try:
    matplotlib.use('TkAgg')
    print("Using TkAgg backend")
except ImportError:
    try:
        matplotlib.use('Qt5Agg')
        print("Using Qt5Agg backend")
    except ImportError:
        print("No GUI backend available")

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.physics import PhysicsEngine
from src.config import get_preset_system
from src.visualization import create_interactive_animation

def test_interactive_animation():
    """Test that interactive animation shows bodies immediately."""
    print("Testing interactive animation initial display...")
    
    # Create engine with inner solar system
    engine = PhysicsEngine(integration_method="rk4")
    engine.set_time_step(86400.0)  # 1 day
    
    bodies = get_preset_system("inner")
    engine.add_bodies(bodies)
    
    print(f"Created {len(bodies)} bodies:")
    AU = 1.496e11
    for body in bodies:
        x_au = body.position.x / AU
        y_au = body.position.y / AU
        z_au = body.position.z / AU
        print(f"  {body.name}: ({x_au:.3f}, {y_au:.3f}, {z_au:.3f}) AU, color: {body.color}")
    
    # Create interactive animation
    print("\nCreating interactive animation...")
    animation = create_interactive_animation(engine, update_interval=100)
    
    # Check that the plotter has the correct setup
    print(f"Plotter auto_scale: {animation.plotter.auto_scale}")
    print(f"Plotter show_trails: {animation.plotter.show_trails}")
    print(f"Animation is_paused: {animation.is_paused}")
    
    # Manually call the update frame to see if it works
    print("\nTesting frame update...")
    try:
        animation._update_frame(0)
        print("✅ Frame update successful")
        
        # Check axis limits after update
        xlim = animation.plotter.ax.get_xlim()
        ylim = animation.plotter.ax.get_ylim()
        zlim = animation.plotter.ax.get_zlim()
        
        print(f"Plot limits after update:")
        print(f"  X: {xlim[0]:.3f} to {xlim[1]:.3f} AU")
        print(f"  Y: {ylim[0]:.3f} to {ylim[1]:.3f} AU")
        print(f"  Z: {zlim[0]:.3f} to {zlim[1]:.3f} AU")
        
        # Check if any scatter plots were created
        children = animation.plotter.ax.get_children()
        scatter_plots = [child for child in children if hasattr(child, 'get_offsets')]
        print(f"Number of scatter plots (bodies): {len(scatter_plots)}")
        
        if len(scatter_plots) >= len(bodies):
            print("✅ Bodies should be visible in the animation")
            return True
        else:
            print("❌ Bodies may not be visible")
            return False
            
    except Exception as e:
        print(f"❌ Frame update failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run interactive animation test."""
    print("=" * 60)
    print("Interactive Animation Fix Test")
    print("=" * 60)
    
    try:
        result = test_interactive_animation()
        
        print("\n" + "=" * 60)
        if result:
            print("✅ INTERACTIVE ANIMATION FIX SUCCESSFUL!")
            print("Bodies should now be visible immediately when the animation starts.")
        else:
            print("❌ INTERACTIVE ANIMATION STILL HAS ISSUES")
        print("=" * 60)
        
        return result
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)