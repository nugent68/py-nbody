"""
Configuration parameters for n-body simulation.
"""
import yaml
import json
from typing import Dict, Any, Optional
from pathlib import Path


class SimulationParameters:
    """
    Class to manage simulation parameters and configuration.
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize simulation parameters.
        
        Args:
            config_file: Path to configuration file (YAML or JSON)
        """
        # Default parameters
        self.defaults = {
            'simulation': {
                'time_step': 86400.0,  # 1 day in seconds
                'integration_method': 'rk4',  # 'euler', 'rk4', 'leapfrog'
                'force_method': 'standard',  # 'standard', 'softened'
                'max_steps': None,
                'max_time': None,
                'softening_length': 0.0
            },
            'system': {
                'preset': 'inner',  # 'inner', 'full', 'earth_moon', 'custom'
                'scale_factor': 1.0,
                'time_scale': 1.0,
                'custom_bodies': []
            },
            'visualization': {
                'show_trails': True,
                'trail_length': 100,
                'update_interval': 50,  # milliseconds
                'figure_size': [12, 9],
                'show_grid': True,
                'show_axes': True,
                'background_color': 'black',
                'auto_scale': True,
                'fixed_scale': None
            },
            'output': {
                'save_data': False,
                'output_directory': 'output',
                'save_interval': 100,  # steps
                'save_format': 'csv',  # 'csv', 'json', 'hdf5'
                'save_trajectories': True,
                'save_energy': True
            },
            'performance': {
                'max_fps': 30,
                'adaptive_time_step': False,
                'parallel_force_calculation': False,
                'memory_limit_mb': 1000
            }
        }
        
        self.config = self.defaults.copy()
        
        if config_file:
            self.load_config(config_file)
    
    def load_config(self, config_file: str) -> None:
        """
        Load configuration from file.
        
        Args:
            config_file: Path to configuration file
        """
        config_path = Path(config_file)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_file}")
        
        try:
            with open(config_path, 'r') as f:
                if config_path.suffix.lower() in ['.yaml', '.yml']:
                    loaded_config = yaml.safe_load(f)
                elif config_path.suffix.lower() == '.json':
                    loaded_config = json.load(f)
                else:
                    raise ValueError(f"Unsupported config file format: {config_path.suffix}")
            
            # Merge with defaults
            self._merge_config(self.config, loaded_config)
            
        except Exception as e:
            raise ValueError(f"Error loading configuration file: {e}")
    
    def save_config(self, config_file: str) -> None:
        """
        Save current configuration to file.
        
        Args:
            config_file: Path to save configuration file
        """
        config_path = Path(config_file)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(config_path, 'w') as f:
                if config_path.suffix.lower() in ['.yaml', '.yml']:
                    yaml.dump(self.config, f, default_flow_style=False, indent=2)
                elif config_path.suffix.lower() == '.json':
                    json.dump(self.config, f, indent=2)
                else:
                    raise ValueError(f"Unsupported config file format: {config_path.suffix}")
                    
        except Exception as e:
            raise ValueError(f"Error saving configuration file: {e}")
    
    def _merge_config(self, base: Dict[str, Any], update: Dict[str, Any]) -> None:
        """
        Recursively merge configuration dictionaries.
        
        Args:
            base: Base configuration dictionary
            update: Update configuration dictionary
        """
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    
    def get(self, key_path: str, default=None):
        """
        Get configuration value using dot notation.
        
        Args:
            key_path: Dot-separated key path (e.g., 'simulation.time_step')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any) -> None:
        """
        Set configuration value using dot notation.
        
        Args:
            key_path: Dot-separated key path
            value: Value to set
        """
        keys = key_path.split('.')
        config = self.config
        
        # Navigate to the parent dictionary
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        # Set the final value
        config[keys[-1]] = value
    
    def validate(self) -> bool:
        """
        Validate configuration parameters.
        
        Returns:
            True if configuration is valid
            
        Raises:
            ValueError: If configuration is invalid
        """
        # Validate integration method
        valid_integrators = ['euler', 'rk4', 'leapfrog']
        integrator = self.get('simulation.integration_method')
        if integrator not in valid_integrators:
            raise ValueError(f"Invalid integration method: {integrator}. "
                           f"Valid options: {valid_integrators}")
        
        # Validate force method
        valid_force_methods = ['standard', 'softened']
        force_method = self.get('simulation.force_method')
        if force_method not in valid_force_methods:
            raise ValueError(f"Invalid force method: {force_method}. "
                           f"Valid options: {valid_force_methods}")
        
        # Validate time step
        time_step = self.get('simulation.time_step')
        if time_step <= 0:
            raise ValueError("Time step must be positive")
        
        # Validate system preset
        valid_presets = ['inner', 'full', 'earth_moon', 'custom']
        preset = self.get('system.preset')
        if preset not in valid_presets:
            raise ValueError(f"Invalid system preset: {preset}. "
                           f"Valid options: {valid_presets}")
        
        # Validate scale factors
        scale_factor = self.get('system.scale_factor')
        if scale_factor <= 0:
            raise ValueError("Scale factor must be positive")
        
        time_scale = self.get('system.time_scale')
        if time_scale <= 0:
            raise ValueError("Time scale must be positive")
        
        return True
    
    def get_simulation_config(self) -> Dict[str, Any]:
        """Get simulation-specific configuration."""
        return self.config.get('simulation', {})
    
    def get_system_config(self) -> Dict[str, Any]:
        """Get system-specific configuration."""
        return self.config.get('system', {})
    
    def get_visualization_config(self) -> Dict[str, Any]:
        """Get visualization-specific configuration."""
        return self.config.get('visualization', {})
    
    def get_output_config(self) -> Dict[str, Any]:
        """Get output-specific configuration."""
        return self.config.get('output', {})
    
    def get_performance_config(self) -> Dict[str, Any]:
        """Get performance-specific configuration."""
        return self.config.get('performance', {})
    
    def __str__(self) -> str:
        """String representation of configuration."""
        return f"SimulationParameters(integrator={self.get('simulation.integration_method')}, " \
               f"preset={self.get('system.preset')}, " \
               f"time_step={self.get('simulation.time_step')})"


def create_default_config_file(filename: str = "config.yaml") -> None:
    """
    Create a default configuration file.
    
    Args:
        filename: Name of the configuration file to create
    """
    params = SimulationParameters()
    params.save_config(filename)


def load_config_from_file(filename: str) -> SimulationParameters:
    """
    Load configuration from file.
    
    Args:
        filename: Path to configuration file
        
    Returns:
        SimulationParameters object
    """
    return SimulationParameters(filename)