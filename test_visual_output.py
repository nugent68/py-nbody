#!/usr/bin/env python3
"""
Test script to create a static image file to verify visualization is working.
"""
import sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.physics import PhysicsEngine
from src.config import get_preset_system
from src.visualization import create_static_plot

def test_static_image_generation():
    """Test generating a static image file."""
    print("Testing static image generation...")
    
    # Create engine with inner solar system
    engine = PhysicsEngine(integration_method="rk4")
    engine.set_time_step(86400.0 * 5)  # 5 days per step
    
    bodies = get_preset_system("inner")
    engine.add_bodies(bodies)
    
    print(f"Created {len(bodies)} bodies:")
    AU = 1.496e11  # meters
    
    for body in bodies:
        x_au = body.position.x / AU
        y_au = body.position.y / AU
        z_au = body.position.z / AU
        print(f"  {body.name}: ({x_au:.3f}, {y_au:.3f}, {z_au:.3f}) AU")
        print(f"    Color: {body.color}, Mass: {body.mass:.2e} kg")
    
    # Run simulation to generate some trajectory data
    print("\nRunning simulation for 30 steps...")
    engine.run(steps=30)
    
    print("Trajectory lengths after simulation:")
    for body in engine.bodies:
        print(f"  {body.name}: {len(body.trajectory)} points")
    
    # Create static plot
    print("\nCreating static plot...")
    plotter = create_static_plot(engine.bodies, engine, show_trails=True, show_labels=True)
    
    # Get plot information
    xlim = plotter.ax.get_xlim()
    ylim = plotter.ax.get_ylim()
    zlim = plotter.ax.get_zlim()
    
    print(f"Plot limits (AU):")
    print(f"  X: {xlim[0]:.3f} to {xlim[1]:.3f}")
    print(f"  Y: {ylim[0]:.3f} to {ylim[1]:.3f}")
    print(f"  Z: {zlim[0]:.3f} to {zlim[1]:.3f}")
    
    # Save the plot
    output_file = "solar_system_test.png"
    print(f"\nSaving plot to {output_file}...")
    plotter.save_plot(output_file, dpi=150)
    
    # Check if file was created
    if Path(output_file).exists():
        file_size = Path(output_file).stat().st_size
        print(f"✅ Image saved successfully! File size: {file_size} bytes")
        
        # Also try to get some info about what was plotted
        print("\nChecking plot contents...")
        
        # Get all the children (plot elements) from the axes
        children = plotter.ax.get_children()
        scatter_plots = [child for child in children if hasattr(child, 'get_offsets')]
        line_plots = [child for child in children if hasattr(child, 'get_data')]
        
        print(f"Found {len(scatter_plots)} scatter plot elements (bodies)")
        print(f"Found {len(line_plots)} line plot elements (trails)")
        
        return True
    else:
        print("❌ Image file was not created")
        return False

def test_simple_matplotlib():
    """Test basic matplotlib functionality."""
    print("\n" + "="*50)
    print("Testing basic matplotlib functionality...")
    
    # Create a simple test plot
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot some test points
    x = [0, 1, 2]
    y = [0, 1, 2] 
    z = [0, 1, 2]
    colors = ['red', 'green', 'blue']
    
    ax.scatter(x, y, z, c=colors, s=100)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Test 3D Plot')
    
    # Save test plot
    test_file = "matplotlib_test.png"
    fig.savefig(test_file, dpi=150, bbox_inches='tight')
    plt.close(fig)
    
    if Path(test_file).exists():
        file_size = Path(test_file).stat().st_size
        print(f"✅ Basic matplotlib test passed! File size: {file_size} bytes")
        return True
    else:
        print("❌ Basic matplotlib test failed")
        return False

def main():
    """Run visualization tests."""
    print("=" * 60)
    print("Visual Output Test Suite")
    print("=" * 60)
    
    try:
        # Test basic matplotlib
        result1 = test_simple_matplotlib()
        
        # Test our simulation visualization
        result2 = test_static_image_generation()
        
        print("\n" + "=" * 60)
        if result1 and result2:
            print("✅ ALL VISUAL TESTS PASSED!")
            print("Check the generated PNG files to see the visualization output.")
        else:
            print("❌ SOME VISUAL TESTS FAILED!")
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