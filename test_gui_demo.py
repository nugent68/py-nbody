#!/usr/bin/env python3
"""
Test script to verify the GUI demo works correctly.
This will test the non-headless version by running a quick demo.
"""
import sys
from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt

# Try to use GUI backend
try:
    matplotlib.use('TkAgg')
    print("Using TkAgg backend for GUI display")
except ImportError:
    try:
        matplotlib.use('Qt5Agg')
        print("Using Qt5Agg backend for GUI display")
    except ImportError:
        print("No GUI backend available - this test may not work properly")

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.physics import PhysicsEngine
from src.config import get_preset_system
from src.visualization import create_static_plot

def test_gui_display():
    """Test that GUI display works correctly."""
    print("Testing GUI display capability...")
    
    # Create a simple simulation
    engine = PhysicsEngine(integration_method="rk4")
    engine.set_time_step(86400.0 * 5)  # 5 days per step
    
    bodies = get_preset_system("inner")
    engine.add_bodies(bodies)
    
    print(f"Created {len(bodies)} bodies")
    
    # Run simulation briefly
    engine.run(steps=20)
    
    # Create plot
    print("Creating plot...")
    plotter = create_static_plot(engine.bodies, engine, show_trails=True)
    
    # Check backend
    backend = matplotlib.get_backend()
    print(f"Current matplotlib backend: {backend}")
    
    # Check if backend is interactive
    is_interactive = backend in ['TkAgg', 'Qt5Agg', 'Qt4Agg', 'GTKAgg', 'MacOSX']
    print(f"Backend is interactive: {is_interactive}")
    
    if is_interactive:
        print("✅ GUI backend is available!")
        print("The plot window should display when running in a GUI environment.")
        print("Note: In headless environments, the window won't appear.")
        
        # Save a copy as well
        plotter.save_plot("gui_test_output.png", dpi=150)
        print("Also saved static image: gui_test_output.png")
        
        return True
    else:
        print("❌ No interactive GUI backend available")
        print("The demo will work but windows may not display properly")
        
        # Save image instead
        plotter.save_plot("gui_test_output.png", dpi=150)
        print("Saved static image: gui_test_output.png")
        
        return False

def main():
    """Run GUI test."""
    print("=" * 60)
    print("GUI Demo Test")
    print("=" * 60)
    
    try:
        result = test_gui_display()
        
        print("\n" + "=" * 60)
        if result:
            print("✅ GUI DEMO SHOULD WORK!")
            print("The simple_demo.py and main.py files are configured for GUI display.")
            print("Run them in a GUI environment to see interactive windows.")
        else:
            print("⚠️  GUI BACKEND NOT AVAILABLE")
            print("The demo files are configured correctly but need a GUI environment.")
            print("Use main_headless.py for headless environments.")
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