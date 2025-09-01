# py-nbody

A Python-based 3D n-body gravitational simulation for modeling planets orbiting a star. This educational and research tool provides realistic physics simulation with interactive 3D visualization.

## Features

### 🌟 Core Physics
- **Newtonian Gravitational Interactions**: Full n-body gravitational force calculations
- **Multiple Integration Methods**: Euler, Runge-Kutta 4th order (RK4), and Leapfrog integrators
- **Energy Conservation**: Built-in validation of energy and momentum conservation
- **Realistic Solar System**: Accurate masses, distances, and orbital parameters

### 🎮 Interactive Visualization
- **Real-time 3D Animation**: Interactive matplotlib-based visualization
- **Orbital Trails**: Configurable trail lengths showing planetary paths
- **Play/Pause Controls**: Start, stop, and reset simulation
- **Speed Control**: Adjust simulation speed with slider
- **Camera Controls**: Rotate, zoom, and pan the 3D view

### ⚙️ Configuration System
- **Preset Solar Systems**: Inner planets, full solar system, Earth-Moon system
- **Custom Scenarios**: Define your own celestial body configurations
- **YAML/JSON Config**: Save and load simulation parameters
- **Scaling Options**: Adjust distance and time scales for different scenarios

### 📊 Analysis Tools
- **Energy Monitoring**: Track kinetic, potential, and total energy over time
- **Conservation Validation**: Verify physics accuracy through conservation laws
- **Performance Metrics**: Real-time FPS and simulation statistics

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Required Packages
- `numpy` - Numerical computations
- `matplotlib` - 3D visualization and animation
- `scipy` - Advanced numerical methods
- `PyYAML` - Configuration file support

## Quick Start

### Run Interactive Simulation
```bash
python main.py --mode interactive --preset inner
```

### Run Quick Demo
```bash
python main.py --mode demo
```

### Command Line Options
```bash
python main.py --help
```

Available options:
- `--preset`: Choose system (`inner`, `full`, `earth_moon`)
- `--integrator`: Integration method (`euler`, `rk4`, `leapfrog`)
- `--time-step`: Time step in seconds (default: 86400 = 1 day)
- `--mode`: Simulation mode (`interactive`, `static`, `demo`)
- `--config`: Load configuration from file

## Usage Examples

### 1. Inner Solar System with RK4 Integration
```bash
python main.py --preset inner --integrator rk4 --mode interactive
```

### 2. Full Solar System with Custom Time Step
```bash
python main.py --preset full --time-step 43200 --mode interactive
```

### 3. Earth-Moon System
```bash
python main.py --preset earth_moon --time-step 3600 --mode interactive
```

### 4. Static Plot Generation
```bash
python main.py --preset inner --mode static --steps 1000
```

## Programming Interface

### Basic Usage
```python
from src.physics import PhysicsEngine
from src.config import get_preset_system
from src.visualization import create_interactive_animation

# Create physics engine
engine = PhysicsEngine(integration_method="rk4")
engine.set_time_step(86400.0)  # 1 day

# Add solar system bodies
bodies = get_preset_system("inner")
engine.add_bodies(bodies)

# Create interactive visualization
animation = create_interactive_animation(engine)
animation.show()
```

### Custom Solar System
```python
from src.physics import Body, Vector3D, PhysicsEngine
from src.visualization import quick_plot

# Create custom bodies
sun = Body(mass=1.989e30, position=Vector3D(0, 0, 0), 
           velocity=Vector3D(0, 0, 0), name="Sun", color="yellow")

earth = Body(mass=5.972e24, position=Vector3D(1.496e11, 0, 0),
             velocity=Vector3D(0, 29780, 0), name="Earth", color="blue")

# Setup simulation
engine = PhysicsEngine()
engine.add_bodies([sun, earth])
engine.run(steps=365)  # Run for 365 steps

# Visualize results
quick_plot(engine.bodies, show_trails=True)
```

## Project Structure

```
py-nbody/
├── src/
│   ├── physics/           # Core physics engine
│   │   ├── vector3d.py    # 3D vector operations
│   │   ├── body.py        # Celestial body class
│   │   ├── integrators.py # Numerical integration methods
│   │   ├── forces.py      # Gravitational force calculations
│   │   └── engine.py      # Main physics engine
│   ├── config/            # Configuration system
│   │   ├── solar_system.py # Solar system presets
│   │   └── parameters.py   # Parameter management
│   └── visualization/     # 3D visualization
│       ├── plotter3d.py   # 3D plotting system
│       └── animation.py   # Interactive animation
├── main.py               # Main application
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Physics Implementation

### Gravitational Forces
The simulation uses Newton's law of universal gravitation:

```
F = G * m₁ * m₂ / r² * r̂
```

Where:
- `G` = 6.674×10⁻¹¹ m³/kg⋅s² (gravitational constant)
- `m₁, m₂` = masses of the two bodies
- `r` = distance between bodies
- `r̂` = unit vector pointing from body 1 to body 2

### Integration Methods

#### Euler Method
Simple first-order integration:
```
v(t+dt) = v(t) + a(t) * dt
r(t+dt) = r(t) + v(t) * dt
```

#### Runge-Kutta 4th Order (RK4)
Higher accuracy fourth-order method using four derivative evaluations per step.

#### Leapfrog Integration
Symplectic integrator that conserves energy well for orbital mechanics.

### Conservation Laws
The simulation validates:
- **Energy Conservation**: Total energy should remain constant
- **Momentum Conservation**: Total linear momentum should be conserved
- **Angular Momentum Conservation**: Total angular momentum should be conserved

## Configuration Files

Create YAML configuration files for custom scenarios:

```yaml
simulation:
  time_step: 86400.0
  integration_method: "rk4"
  max_steps: 10000

system:
  preset: "inner"
  scale_factor: 1.0
  time_scale: 1.0

visualization:
  show_trails: true
  trail_length: 100
  figure_size: [12, 9]
  background_color: "black"
```

## Performance Considerations

### Computational Complexity
- **Force Calculation**: O(n²) for n bodies
- **Integration**: O(n) per time step
- **Visualization**: Depends on trail length and update frequency

### Optimization Tips
1. **Reduce Time Step**: Smaller steps = higher accuracy but slower simulation
2. **Limit Trail Length**: Shorter trails = better performance
3. **Choose Integration Method**: Euler (fast) vs RK4 (accurate)
4. **Scale Factors**: Use appropriate scaling for your scenario

## Validation and Accuracy

### Energy Conservation Test
```python
# Check energy conservation
analysis = engine.get_conservation_analysis()
energy_drift = analysis['energy']['drift_percent']
print(f"Energy drift: {energy_drift:.6f}%")
```

### Orbital Period Validation
The simulation can be validated against Kepler's laws:
- **Kepler's 3rd Law**: T² ∝ a³ (period squared proportional to semi-major axis cubed)

## Educational Applications

### Learning Objectives
- **Orbital Mechanics**: Understand how planets orbit stars
- **Numerical Methods**: Compare different integration techniques
- **Conservation Laws**: Observe energy and momentum conservation
- **Gravitational Physics**: Visualize n-body gravitational interactions

### Suggested Experiments
1. **Compare Integrators**: Run same scenario with different integration methods
2. **Energy Conservation**: Monitor energy drift over long simulations
3. **Orbital Resonances**: Set up planets in resonant configurations
4. **Three-Body Problem**: Explore chaotic dynamics with three massive bodies

## Troubleshooting

### Common Issues

#### Import Errors
```bash
# Ensure you're running from the project root directory
python main.py

# Or add the src directory to Python path
export PYTHONPATH="${PYTHONPATH}:./src"
```

#### Performance Issues
- Reduce trail length: `--trail-length 50`
- Use Euler integration: `--integrator euler`
- Increase time step: `--time-step 172800` (2 days)

#### Visualization Problems
- Update matplotlib: `pip install --upgrade matplotlib`
- Check display settings for 3D rendering
- Try different backends: `matplotlib.use('TkAgg')`

## Contributing

### Development Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run tests: `python -m pytest tests/` (when available)

### Code Structure
- Follow PEP 8 style guidelines
- Add docstrings to all functions and classes
- Include type hints where appropriate
- Write unit tests for new features

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Physics equations based on Newton's laws of gravitation
- Solar system data from NASA/JPL ephemeris
- Visualization powered by matplotlib
- Numerical integration methods from computational physics literature

## Future Enhancements

- [ ] Relativistic corrections for high-precision simulations
- [ ] Collision detection and handling
- [ ] Variable time stepping for adaptive accuracy
- [ ] GPU acceleration for large n-body systems
- [ ] Export capabilities for data analysis
- [ ] Web-based interface using matplotlib widgets
