"""
Animation system with interactive controls for n-body simulation.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, Slider
import threading
import time
from typing import List, Optional, Callable, Dict, Any
from ..physics import PhysicsEngine, Body
from .plotter3d import Plotter3D


class InteractiveAnimation:
    """
    Interactive 3D animation system for n-body simulation.
    """
    
    def __init__(self, 
                 engine: PhysicsEngine,
                 update_interval: int = 50,
                 steps_per_frame: int = 1,
                 figure_size: tuple = (14, 10)):
        """
        Initialize interactive animation.
        
        Args:
            engine: PhysicsEngine instance
            update_interval: Animation update interval in milliseconds
            steps_per_frame: Number of simulation steps per animation frame
            figure_size: Figure size (width, height)
        """
        self.engine = engine
        self.update_interval = update_interval
        self.steps_per_frame = steps_per_frame
        
        # Animation state
        self.is_playing = False
        self.is_paused = True
        self.animation = None
        self.frame_count = 0
        
        # Create figure with subplots for controls
        self.fig = plt.figure(figsize=figure_size, facecolor='black')
        
        # Main 3D plot (takes most of the space)
        self.ax_main = self.fig.add_subplot(111, projection='3d')
        
        # Create plotter for 3D visualization with proper initialization
        self.plotter = Plotter3D(figure_size=figure_size, background_color='black')
        # Replace the plotter's figure and axis with our animation figure
        plt.close(self.plotter.fig)  # Close the plotter's original figure
        self.plotter.fig = self.fig
        self.plotter.ax = self.ax_main
        self.plotter._setup_axes()
        
        # Control panel
        self._setup_controls()
        
        # Performance tracking
        self.fps_history = []
        self.last_frame_time = time.time()
        
        # Callback functions
        self.frame_callback = None
        self.pause_callback = None
        self.reset_callback = None
    
    def _setup_controls(self) -> None:
        """Setup interactive control widgets."""
        # Adjust main plot to make room for controls
        plt.subplots_adjust(bottom=0.15, right=0.85)
        
        # Play/Pause button
        ax_play = plt.axes([0.02, 0.02, 0.08, 0.04])
        self.btn_play = Button(ax_play, 'Play', color='lightgreen', hovercolor='green')
        self.btn_play.on_clicked(self._toggle_play_pause)
        
        # Reset button
        ax_reset = plt.axes([0.12, 0.02, 0.08, 0.04])
        self.btn_reset = Button(ax_reset, 'Reset', color='lightcoral', hovercolor='red')
        self.btn_reset.on_clicked(self._reset_simulation)
        
        # Speed slider
        ax_speed = plt.axes([0.25, 0.02, 0.2, 0.03])
        self.slider_speed = Slider(ax_speed, 'Speed', 0.1, 5.0, valinit=1.0, 
                                  facecolor='lightblue')
        self.slider_speed.on_changed(self._update_speed)
        
        # Trail length slider
        ax_trail = plt.axes([0.25, 0.06, 0.2, 0.03])
        self.slider_trail = Slider(ax_trail, 'Trail', 10, 500, valinit=100, 
                                  valfmt='%d', facecolor='lightblue')
        self.slider_trail.on_changed(self._update_trail_length)
        
        # Info text area
        self.info_text = self.ax_main.text2D(0.87, 0.98, "", transform=self.ax_main.transAxes,
                                           verticalalignment='top', color='white', fontsize=9,
                                           bbox=dict(boxstyle='round', facecolor='black', alpha=0.8))
    
    def _toggle_play_pause(self, event) -> None:
        """Toggle between play and pause states."""
        if self.is_paused:
            self.play()
        else:
            self.pause()
    
    def _reset_simulation(self, event) -> None:
        """Reset the simulation to initial state."""
        self.pause()
        self.engine.reset_simulation()
        self.frame_count = 0
        
        if self.reset_callback:
            self.reset_callback()
        
        # Update display
        self._update_frame(0)
    
    def _update_speed(self, val) -> None:
        """Update simulation speed."""
        self.steps_per_frame = max(1, int(val))
    
    def _update_trail_length(self, val) -> None:
        """Update trail length."""
        self.plotter.set_trail_length(int(val))
    
    def play(self) -> None:
        """Start the animation."""
        if not self.is_playing:
            self.is_playing = True
            self.is_paused = False
            self.btn_play.label.set_text('Pause')
            
            # Start animation
            self.animation = FuncAnimation(
                self.fig, self._update_frame, 
                interval=self.update_interval, 
                blit=False, cache_frame_data=False
            )
    
    def pause(self) -> None:
        """Pause the animation."""
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.btn_play.label.set_text('Play')
            
            if self.animation:
                self.animation.pause()
            
            if self.pause_callback:
                self.pause_callback()
    
    def _update_frame(self, frame_num) -> None:
        """
        Update animation frame.
        
        Args:
            frame_num: Frame number (from FuncAnimation)
        """
        # Only advance simulation if not paused
        if not self.is_paused:
            # Run simulation steps
            for _ in range(self.steps_per_frame):
                self.engine.step()
            
            self.frame_count += 1
        
        # Always update visualization (even when paused)
        self.plotter.plot_trajectories(self.engine.bodies, show_labels=True)
        
        # Update info text
        self._update_info_text()
        
        # Track performance
        self._update_performance_stats()
        
        # Call frame callback if provided
        if self.frame_callback:
            self.frame_callback(self.engine, self.frame_count)
        
        # Force redraw
        self.fig.canvas.draw_idle()
    
    def _update_info_text(self) -> None:
        """Update the information text display."""
        # Get system energy
        kinetic, potential, total = self.engine.get_system_energy()
        
        # Calculate FPS
        current_fps = len(self.fps_history) / max(1, len(self.fps_history)) if self.fps_history else 0
        
        # Create info text
        info_lines = [
            f"Time: {self.engine.time:.2e} s",
            f"Steps: {self.engine.step_count}",
            f"Frame: {self.frame_count}",
            f"Bodies: {len(self.engine.bodies)}",
            f"",
            f"Energy (J):",
            f"  Kinetic: {kinetic:.2e}",
            f"  Potential: {potential:.2e}",
            f"  Total: {total:.2e}",
            f"",
            f"Performance:",
            f"  FPS: {current_fps:.1f}",
            f"  Integrator: {self.engine.integrator.name}",
            f"  dt: {self.engine.dt:.2e} s"
        ]
        
        self.info_text.set_text('\n'.join(info_lines))
    
    def _update_performance_stats(self) -> None:
        """Update performance statistics."""
        current_time = time.time()
        frame_time = current_time - self.last_frame_time
        
        if frame_time > 0:
            fps = 1.0 / frame_time
            self.fps_history.append(fps)
            
            # Keep only recent FPS values
            if len(self.fps_history) > 30:
                self.fps_history.pop(0)
        
        self.last_frame_time = current_time
    
    def set_frame_callback(self, callback: Callable) -> None:
        """
        Set callback function called on each frame update.
        
        Args:
            callback: Function with signature callback(engine, frame_count)
        """
        self.frame_callback = callback
    
    def set_pause_callback(self, callback: Callable) -> None:
        """
        Set callback function called when animation is paused.
        
        Args:
            callback: Function with no arguments
        """
        self.pause_callback = callback
    
    def set_reset_callback(self, callback: Callable) -> None:
        """
        Set callback function called when simulation is reset.
        
        Args:
            callback: Function with no arguments
        """
        self.reset_callback = callback
    
    def save_frame(self, filename: str, dpi: int = 300) -> None:
        """
        Save current frame to file.
        
        Args:
            filename: Output filename
            dpi: Resolution in dots per inch
        """
        self.plotter.save_plot(filename, dpi)
    
    def show(self) -> None:
        """Display the animation window."""
        # Ensure the figure is current
        plt.figure(self.fig.number)
        
        # Display initial frame immediately
        self._update_frame(0)
        
        # Force a draw to ensure everything is rendered
        self.fig.canvas.draw()
        
        plt.show()
    
    def close(self) -> None:
        """Close the animation window."""
        if self.animation:
            self.animation.pause()
        plt.close(self.fig)


class SimpleAnimation:
    """
    Simple animation without interactive controls.
    """
    
    def __init__(self, 
                 engine: PhysicsEngine,
                 update_interval: int = 50,
                 steps_per_frame: int = 1):
        """
        Initialize simple animation.
        
        Args:
            engine: PhysicsEngine instance
            update_interval: Animation update interval in milliseconds
            steps_per_frame: Number of simulation steps per animation frame
        """
        self.engine = engine
        self.update_interval = update_interval
        self.steps_per_frame = steps_per_frame
        
        # Create plotter
        self.plotter = Plotter3D()
        
        # Animation
        self.animation = None
        self.frame_count = 0
    
    def _update_frame(self, frame_num) -> None:
        """Update animation frame."""
        # Run simulation steps
        for _ in range(self.steps_per_frame):
            self.engine.step()
        
        self.frame_count += 1
        
        # Update visualization
        self.plotter.plot_trajectories(self.engine.bodies, show_labels=True)
        self.plotter.add_info_text(self.engine)
    
    def run(self, frames: Optional[int] = None) -> None:
        """
        Run the animation.
        
        Args:
            frames: Number of frames to run (None for infinite)
        """
        self.animation = FuncAnimation(
            self.plotter.fig, self._update_frame,
            frames=frames, interval=self.update_interval,
            blit=False, cache_frame_data=False
        )
        
        plt.show()
    
    def save_animation(self, filename: str, frames: int = 100, fps: int = 20) -> None:
        """
        Save animation to file.
        
        Args:
            filename: Output filename
            frames: Number of frames to save
            fps: Frames per second
        """
        self.animation = FuncAnimation(
            self.plotter.fig, self._update_frame,
            frames=frames, interval=self.update_interval,
            blit=False, cache_frame_data=False
        )
        
        # Save animation (requires ffmpeg or pillow)
        try:
            self.animation.save(filename, fps=fps, writer='pillow')
        except Exception as e:
            print(f"Error saving animation: {e}")
            print("Try installing ffmpeg or pillow for animation export")


def create_interactive_animation(engine: PhysicsEngine, **kwargs) -> InteractiveAnimation:
    """
    Create an interactive animation with controls.
    
    Args:
        engine: PhysicsEngine instance
        **kwargs: Additional arguments for InteractiveAnimation
        
    Returns:
        InteractiveAnimation instance
    """
    return InteractiveAnimation(engine, **kwargs)


def create_simple_animation(engine: PhysicsEngine, **kwargs) -> SimpleAnimation:
    """
    Create a simple animation without controls.
    
    Args:
        engine: PhysicsEngine instance
        **kwargs: Additional arguments for SimpleAnimation
        
    Returns:
        SimpleAnimation instance
    """
    return SimpleAnimation(engine, **kwargs)