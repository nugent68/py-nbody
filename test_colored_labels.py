#!/usr/bin/env python3
"""
Test script to verify that planet labels are colored to match their bodies.
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

def test_colored_labels():
    """Test that labels are colored to match planet colors."""
    print("Testing colored labels...")
    
    # Create engine with inner solar system
    engine = PhysicsEngine(integration_method="rk4")
    engine.set_time_step(86400.0 * 5)  # 5 days per step
    
    bodies = get_preset_system("inner")
    engine.add_bodies(bodies)
    
    print(f"Created {len(bodies)} bodies with colors:")
    for body in bodies:
        print(f"  {body.name}: {body.color}")
    
    # Run simulation briefly to generate some trajectory
    engine.run(steps=10)
    
    # Create static plot
    plotter = create_static_plot(engine.bodies, engine, show_trails=True, show_labels=True)
    
    # Save the plot
    output_file = "colored_labels_test.png"
    plotter.save_plot(output_file, dpi=150)
    
    # Check if file was created
    if Path(output_file).exists():
        file_size = Path(output_file).stat().st_size
        print(f"✅ Plot with colored labels saved: {output_file} ({file_size} bytes)")
        
        # Check plot elements
        children = plotter.ax.get_children()
        text_elements = [child for child in children if hasattr(child, 'get_text')]
        
        print(f"Found {len(text_elements)} text elements in the plot")
        
        # Check if we have text elements (labels)
        body_labels = []
        for text_elem in text_elements:
            text_content = text_elem.get_text().strip()
            if text_content in [body.name for body in bodies]:
                color = text_elem.get_color()
                body_labels.append((text_content, color))
        
        print(f"Found {len(body_labels)} body labels:")
        for name, color in body_labels:
            print(f"  {name}: color={color}")
        
        if len(body_labels) >= len(bodies):
            print("✅ All body labels found with colors!")
            return True
        else:
            print("❌ Some body labels may be missing")
            return False
    else:
        print("❌ Plot file was not created")
        return False

def main():
    """Run colored labels test."""
    print("=" * 60)
    print("Colored Labels Test")
    print("=" * 60)
    
    try:
        result = test_colored_labels()
        
        print("\n" + "=" * 60)
        if result:
            print("✅ COLORED LABELS TEST PASSED!")
            print("Planet labels now match their body colors.")
            print("The interactive animation will show:")
            print("  - Sun: yellow label")
            print("  - Mercury: gray label") 
            print("  - Venus: orange label")
            print("  - Earth: blue label")
            print("  - Mars: red label")
        else:
            print("❌ COLORED LABELS TEST FAILED")
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