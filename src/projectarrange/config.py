from pathlib import Path
import tomllib
from typing import Optional, Dict, Any

def load_config(config_path: Optional[Path] = None) -> Dict[str, Any]:
    """Load configuration from a TOML file if provided."""
    if config_path and config_path.exists():
        try:
            with open(config_path, "rb") as f:
                return tomllib.load(f)
        except Exception as e:
            print(f"Warning: Could not load config file: {e}")
    return {}