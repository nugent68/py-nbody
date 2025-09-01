# N-Body Simulation Usage Guide

This guide explains how to run the interactive n-body gravitational simulation in different environments.

## Quick Start

### For GUI Environments (Recommended)

If you have a graphical desktop environment (Windows, macOS, Linux with X11):

```bash
# Run interactive simulation
python main.py --mode interactive --preset inner

# Run simple demo
python examples/simple_demo.py

# Run quick demo
python main.py --mode demo
```

### For Headless Environments (Servers, SSH, etc.)

If you're running on a server or via SSH without GUI:

```bash
# Run headless simulation (saves images)
python main_headless.py --mode animated --preset inner --steps 50

# Run static simulation
python main_headless.py --mode static --preset inner --steps 100

# Run quick demo
python main_headless.py --mode demo
```

## Interactive Features

### GUI Mode Features
- **Real-time 3D Animation**: Interactive matplotlib window with orbital visualization
- **Play/Pause Controls**: Start, stop, and reset simulation
- **Speed Control**: Adjust simulation speed with slider (1x to 5x)
- **Trail Length**: Adjust orbital trail length (10-500 points)
- **3D Navigation**: Mouse controls for rotation, zoom, and pan
- **Real-time Info**: Energy monitoring, step count, FPS tracking

### Headless Mode Features
- **Automatic Image Generation**: Saves PNG files at specified intervals
- **Animation Sequences**: Creates series of images showing orbital evolution
- **Static Plots**: Single high-resolution images of final simulation state
- **Progress Monitoring**: Console output with energy conservation tracking

## System Presets

### Inner Solar System (`--preset inner`)
- **Bodies**: Sun, Mercury, Venus, Earth, Mars
- **Scale**: ~3 AU diameter
- **Recommended time step**: 1 day (86400 seconds)
- **Good for**: Observing planetary orbits, testing energy conservation

### Full Solar System (`--preset full`)
- **Bodies**: Sun + all 8 planets
- **Scale**: ~60 AU diameter
- **Recommended time step**: 1-10 days
- **Good for**: Long-term orbital dynamics, outer planet interactions

### Earth-Moon System (`--preset earth_moon`)
- **Bodies**: Earth, Moon
- **Scale**: ~0.02 AU diameter
- **Recommended time step**: 1 hour (3600 seconds)
- **Good for**: High-precision orbital mechanics, tidal effects

## Integration Methods

### RK4 (Recommended)
```bash
python main.py --integrator rk4
```
- **Accuracy**: High (4th order)
- **Stability**: Excellent
- **Performance**: Moderate
- **Best for**: Most simulations, energy conservation

### Leapfrog
```bash
python main.py --integrator leapfrog
```
- **Accuracy**: Good (2nd order)
- **Stability**: Excellent for orbital mechanics
- **Performance**: Fast
- **Best for**: Long-term simulations, symplectic integration

### Euler
```bash
python main.py --integrator euler
```
- **Accuracy**: Basic (1st order)
- **Stability**: Poor for long simulations
- **Performance**: Fastest
- **Best for**: Quick tests, educational purposes

## Example Commands

### Interactive Simulations
```bash
# Inner solar system with RK4 integration
python main.py --mode interactive --preset inner --integrator rk4

# Earth-Moon system with 1-hour time steps
python main.py --mode interactive --preset earth_moon --time-step 3600

# Full solar system with 5-day time steps
python main.py --mode interactive --preset full --time-step 432000
```

### Headless Simulations
```bash
# Create animation sequence (saves images every 10 steps)
python main_headless.py --mode animated --preset inner --steps 100 --save-interval 10

# Generate high-resolution static plot
python main_headless.py --mode static --preset inner --steps 500 --output solar_system.png

# Quick demo with custom output
python main_headless.py --mode demo --output demo_result.png
```

### Advanced Options
```bash
# Custom time scaling
python main.py --preset inner --time-step 43200 --time-scale 2.0

# Custom distance scaling
python main.py --preset earth_moon --scale-factor 0.5

# Load configuration file
python main.py --config configs/sample_config.yaml
```

## Visualization Features

### Scaling and Units
- **Automatic Scaling**: Plots automatically scale to show all bodies
- **AU Units**: Axes labeled in Astronomical Units for readability
- **Proper Proportions**: Bodies sized appropriately for visibility
- **Trail Visualization**: Orbital paths with fading effects

### Energy Conservation
- **Real-time Monitoring**: Energy values displayed during simulation
- **Conservation Analysis**: Drift percentage calculated automatically
- **Physics Validation**: Confirms simulation accuracy

### Performance Optimization
- **Adaptive Rendering**: Efficient 3D plotting for smooth animation
- **Trail Management**: Configurable trail lengths for performance
- **Frame Rate Control**: Adjustable update intervals

## Troubleshooting

### No GUI Display
If you see "Animation was deleted without rendering anything":
- You're likely in a headless environment
- Use `python main_headless.py` instead
- Or install a GUI backend: `pip install tkinter` or `pip install PyQt5`

### Poor Performance
- Reduce trail length: `--trail-length 50`
- Use Euler integration: `--integrator euler`
- Increase time step: `--time-step 172800` (2 days)

### Energy Drift
- Use RK4 integration: `--integrator rk4`
- Reduce time step: `--time-step 43200` (12 hours)
- Check for numerical instabilities in output

## Output Files

### Headless Mode Outputs
- **Animation sequences**: `animation_<preset>_<integrator>/step_XXX.png`
- **Static plots**: `<preset>_<integrator>_<steps>steps.png`
- **Demo outputs**: `demo_output.png`

### File Formats
- **PNG**: High-quality images with transparency
- **Resolution**: 150-300 DPI for publication quality
- **Size**: Typically 150-200 KB per image

## System Requirements

### Minimum
- Python 3.7+
- 4 GB RAM
- Any CPU (simulation scales with complexity)

### Recommended
- Python 3.9+
- 8 GB RAM
- Multi-core CPU for better performance
- GUI environment for interactive mode

### Dependencies
- numpy >= 1.21.0
- matplotlib >= 3.5.0
- scipy >= 1.7.0
- PyYAML >= 6.0

## Getting Help

```bash
# Show all command line options
python main.py --help
python main_headless.py --help

# Run test suite
python test_simulation.py
python test_scaling.py
python test_visual_output.py
```

For more information, see the main README.md file.