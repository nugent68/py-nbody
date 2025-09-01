#!/usr/bin/env python3
"""
Test script to create a screenshot of the interactive animation to verify bodies are visible.
"""
import sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for screenshot
import matplotlib.pyplot as plt

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.physics import PhysicsEngine
from src.config import get_preset_system
from src.visualization import create_interactive_animation

def test_animation_screenshot():
    """Create a screenshot of the interactive animation."""
    print("Testing interactive animation screenshot...")
    
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
    
    # Update the frame to display bodies
    print("Updating animation frame...")
    animation._update_frame(0)
    
    # Save screenshot
    screenshot_file = "interactive_animation_screenshot.png"
    print(f"Saving screenshot to {screenshot_file}...")
    animation.save_frame(screenshot_file, dpi=150)
    
    # Check if file was created
    if Path(screenshot_file).exists():
        file_size = Path(screenshot_file).stat().st_size
        print(f"✅ Screenshot saved successfully! File size: {file_size} bytes")
        
        # Check plot elements
        children = animation.plotter.ax.get_children()
        scatter_plots = [child for child in children if hasattr(child, 'get_offsets')]
        line_plots = [child for child in children if hasattr(child, 'get_data')]
        
        print(f"Plot elements found:")
        print(f"  Scatter plots (bodies): {len(scatter_plots)}")
        print(f"  Line plots (trails): {len(line_plots)}")
        
        # Get axis limits
        xlim = animation.plotter.ax.get_xlim()
        ylim = animation.plotter.ax.get_ylim()
        zlim = animation.plotter.ax.get_zlim()
        
        print(f"Plot limits (AU):")
        print(f"  X: {xlim[0]:.3f} to {xlim[1]:.3f}")
        print(f"  Y: {ylim[0]:.3f} to {ylim[1]:.3f}")
        print(f"  Z: {zlim[0]:.3f} to {zlim[1]:.3f}")
        
        if len(scatter_plots) >= len(bodies):
            print("✅ Bodies should be visible in the interactive animation!")
            return True
        else:
            print("❌ Bodies may not be visible in the interactive animation")
            return False
    else:
        print("❌ Screenshot file was not created")
        return False

def main():
    """Run animation screenshot test."""
    print("=" * 60)
    print("Interactive Animation Screenshot Test")
    print("=" * 60)
    
    try:
        result = test_animation_screenshot()
        
        print("\n" + "=" * 60)
        if result:
            print("✅ INTERACTIVE ANIMATION IS WORKING!")
            print("Bodies are properly displayed in the animation.")
            print("The interactive simulation should now show planets correctly.")
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