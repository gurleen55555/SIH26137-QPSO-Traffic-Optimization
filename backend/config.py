"""
Backend configuration — reads from environment variables with sane defaults.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment or .env file."""

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    environment: str = "development"
    log_level: str = "info"

    # Geographic defaults (Bengaluru CBD)
    city_name: str = "Bengaluru, Karnataka, India"
    default_lat: float = 12.9716
    default_lon: float = 77.5946
    search_radius_meters: int = 2500

    # Graph
    toy_graph_nodes: int = 15
    default_num_vehicles: int = 3
    default_vehicle_capacity: float = 100.0
    default_num_destinations: int = 10

    model_config = {"env_file": ".env", "case_sensitive": False}


settings = Settings()
