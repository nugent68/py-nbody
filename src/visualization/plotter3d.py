"""
3D plotting and visualization for n-body simulation.
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from typing import List, Optional, Dict, Any, Tuple
from ..physics import Body, PhysicsEngine


class Plotter3D:
    """
    3D visualization system for n-body simulation.
    """
    
    def __init__(self, 
                 figure_size: Tuple[int, int] = (12, 9),
                 background_color: str = 'black',
                 show_grid: bool = True,
                 show_axes: bool = True):
        """
        Initialize the 3D plotter.
        
        Args:
            figure_size: Figure size (width, height)
            background_color: Background color
            show_grid: Whether to show grid
            show_axes: Whether to show axes
        """
        self.figure_size = figure_size
        self.background_color = background_color
        self.show_grid = show_grid
        self.show_axes = show_axes
        
        # Create figure and 3D axis
        self.fig = plt.figure(figsize=figure_size, facecolor=background_color)
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_facecolor(background_color)
        
        # Visualization settings
        self.trail_length = 100
        self.show_trails = True
        self.auto_scale = True
        self.fixed_scale = None
        self.body_scale_factor = 1.0
        
        # Plot elements
        self.body_plots = {}
        self.trail_plots = {}
        self.text_labels = {}
        
        # Setup initial appearance
        self._setup_axes()
    
    def _setup_axes(self) -> None:
        """Setup 3D axes appearance."""
        if self.show_grid:
            self.ax.grid(True, alpha=0.3)
        else:
            self.ax.grid(False)
        
        if not self.show_axes:
            self.ax.set_axis_off()
        
        # Set labels
        self.ax.set_xlabel('X (m)', color='white')
        self.ax.set_ylabel('Y (m)', color='white')
        self.ax.set_zlabel('Z (m)', color='white')
        
        # Set tick colors
        self.ax.tick_params(colors='white')
        
        # Set title
        self.ax.set_title('N-Body Gravitational Simulation', color='white', fontsize=14)
    
    def set_trail_length(self, length: int) -> None:
        """
        Set the length of orbital trails.
        
        Args:
            length: Number of points in trail
        """
        self.trail_length = length
    
    def set_show_trails(self, show: bool) -> None:
        """
        Enable or disable orbital trails.
        
        Args:
            show: Whether to show trails
        """
        self.show_trails = show
    
    def set_auto_scale(self, auto: bool, fixed_scale: Optional[float] = None) -> None:
        """
        Set scaling mode for the plot.
        
        Args:
            auto: Whether to use automatic scaling
            fixed_scale: Fixed scale value (if auto is False)
        """
        self.auto_scale = auto
        self.fixed_scale = fixed_scale
    
    def set_body_scale_factor(self, factor: float) -> None:
        """
        Set scaling factor for body sizes.
        
        Args:
            factor: Scale factor for body visualization
        """
        self.body_scale_factor = factor
    
    def plot_bodies(self, bodies: List[Body], show_labels: bool = True) -> None:
        """
        Plot celestial bodies at their current positions.
        
        Args:
            bodies: List of Body objects
            show_labels: Whether to show body name labels
        """
        # Clear previous plots
        self.ax.clear()
        self._setup_axes()
        
        # Plot each body
        for body in bodies:
            self._plot_single_body(body, show_labels)
        
        # Update scaling
        self._update_scaling(bodies)
        
        plt.draw()
    
    def _plot_single_body(self, body: Body, show_label: bool = True) -> None:
        """
        Plot a single celestial body.
        
        Args:
            body: Body object to plot
            show_label: Whether to show body label
        """
        # Calculate visual size (logarithmic scaling for better visibility)
        base_size = 50
        if body.name.lower() == 'sun':
            size = base_size * 3 * self.body_scale_factor
        else:
            size = base_size * self.body_scale_factor
        
        # Plot body as a sphere
        self.ax.scatter(body.position.x, body.position.y, body.position.z,
                       c=body.color, s=size, alpha=0.8, edgecolors='white', linewidth=0.5)
        
        # Add label
        if show_label:
            self.ax.text(body.position.x, body.position.y, body.position.z,
                        f'  {body.name}', color='white', fontsize=8)
    
    def plot_trajectories(self, bodies: List[Body], show_labels: bool = True) -> None:
        """
        Plot bodies with their orbital trajectories.
        
        Args:
            bodies: List of Body objects
            show_labels: Whether to show body name labels
        """
        # Clear previous plots
        self.ax.clear()
        self._setup_axes()
        
        # Plot trajectories and bodies
        for body in bodies:
            self._plot_trajectory(body)
            self._plot_single_body(body, show_labels)
        
        # Update scaling
        self._update_scaling(bodies)
        
        plt.draw()
    
    def _plot_trajectory(self, body: Body) -> None:
        """
        Plot trajectory trail for a single body.
        
        Args:
            body: Body object
        """
        if not self.show_trails or len(body.trajectory) < 2:
            return
        
        # Get trajectory coordinates
        x_coords, y_coords, z_coords = body.get_trajectory_arrays()
        
        # Limit trail length
        if len(x_coords) > self.trail_length:
            x_coords = x_coords[-self.trail_length:]
            y_coords = y_coords[-self.trail_length:]
            z_coords = z_coords[-self.trail_length:]
        
        # Plot trail with fading effect
        if len(x_coords) > 1:
            # Create alpha values for fading effect
            alphas = np.linspace(0.1, 0.8, len(x_coords))
            
            # Plot trail segments
            for i in range(len(x_coords) - 1):
                self.ax.plot([x_coords[i], x_coords[i+1]],
                           [y_coords[i], y_coords[i+1]],
                           [z_coords[i], z_coords[i+1]],
                           color=body.color, alpha=alphas[i], linewidth=1)
    
    def _update_scaling(self, bodies: List[Body]) -> None:
        """
        Update plot scaling based on body positions.
        
        Args:
            bodies: List of Body objects
        """
        if not bodies:
            return
        
        if self.auto_scale:
            # Calculate bounds from all body positions and trajectories
            all_x, all_y, all_z = [], [], []
            
            for body in bodies:
                all_x.append(body.position.x)
                all_y.append(body.position.y)
                all_z.append(body.position.z)
                
                # Include trajectory points
                if self.show_trails and body.trajectory:
                    x_traj, y_traj, z_traj = body.get_trajectory_arrays()
                    all_x.extend(x_traj)
                    all_y.extend(y_traj)
                    all_z.extend(z_traj)
            
            # Calculate bounds with some padding
            if all_x and all_y and all_z:
                x_range = max(all_x) - min(all_x)
                y_range = max(all_y) - min(all_y)
                z_range = max(all_z) - min(all_z)
                
                max_range = max(x_range, y_range, z_range)
                padding = max_range * 0.1
                
                center_x = (max(all_x) + min(all_x)) / 2
                center_y = (max(all_y) + min(all_y)) / 2
                center_z = (max(all_z) + min(all_z)) / 2
                
                half_range = max_range / 2 + padding
                
                self.ax.set_xlim(center_x - half_range, center_x + half_range)
                self.ax.set_ylim(center_y - half_range, center_y + half_range)
                self.ax.set_zlim(center_z - half_range, center_z + half_range)
        
        elif self.fixed_scale is not None:
            # Use fixed scaling
            self.ax.set_xlim(-self.fixed_scale, self.fixed_scale)
            self.ax.set_ylim(-self.fixed_scale, self.fixed_scale)
            self.ax.set_zlim(-self.fixed_scale, self.fixed_scale)
    
    def add_info_text(self, engine: PhysicsEngine) -> None:
        """
        Add simulation information text to the plot.
        
        Args:
            engine: PhysicsEngine instance
        """
        # Get system energy
        kinetic, potential, total = engine.get_system_energy()
        
        # Create info text
        info_text = f"Time: {engine.time:.2e} s\n"
        info_text += f"Steps: {engine.step_count}\n"
        info_text += f"Bodies: {len(engine.bodies)}\n"
        info_text += f"Total Energy: {total:.2e} J\n"
        info_text += f"Integrator: {engine.integrator.name}"
        
        # Add text to plot
        self.ax.text2D(0.02, 0.98, info_text, transform=self.ax.transAxes,
                      verticalalignment='top', color='white', fontsize=10,
                      bbox=dict(boxstyle='round', facecolor='black', alpha=0.7))
    
    def save_plot(self, filename: str, dpi: int = 300) -> None:
        """
        Save the current plot to file.
        
        Args:
            filename: Output filename
            dpi: Resolution in dots per inch
        """
        self.fig.savefig(filename, dpi=dpi, facecolor=self.background_color,
                        bbox_inches='tight')
    
    def show(self) -> None:
        """Display the plot."""
        plt.show()
    
    def close(self) -> None:
        """Close the plot."""
        plt.close(self.fig)


def create_static_plot(bodies: List[Body], 
                      engine: Optional[PhysicsEngine] = None,
                      show_trails: bool = True,
                      show_labels: bool = True,
                      title: str = "N-Body Simulation") -> Plotter3D:
    """
    Create a static 3D plot of the current system state.
    
    Args:
        bodies: List of Body objects
        engine: Optional PhysicsEngine for additional info
        show_trails: Whether to show orbital trails
        show_labels: Whether to show body labels
        title: Plot title
        
    Returns:
        Plotter3D instance
    """
    plotter = Plotter3D()
    plotter.set_show_trails(show_trails)
    plotter.ax.set_title(title, color='white', fontsize=14)
    
    if show_trails:
        plotter.plot_trajectories(bodies, show_labels)
    else:
        plotter.plot_bodies(bodies, show_labels)
    
    if engine:
        plotter.add_info_text(engine)
    
    return plotter


def quick_plot(bodies: List[Body], show_trails: bool = True) -> None:
    """
    Quick plot function for immediate visualization.
    
    Args:
        bodies: List of Body objects
        show_trails: Whether to show orbital trails
    """
    plotter = create_static_plot(bodies, show_trails=show_trails)
    plotter.show()