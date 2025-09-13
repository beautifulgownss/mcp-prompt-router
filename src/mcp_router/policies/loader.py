from pathlib import Path
from typing import Any, Dict
import yaml

POLICY_DIR = Path(__file__).parent

def load_policy(filename: str = "fast-cheap-safe.yaml") -> Dict[str, Any]:
    path = POLICY_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Policy file not found: {path}")
    with path.open("r") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict) or "profiles" not in data:
        raise ValueError("Invalid policy file: missing 'profiles'")
    return data
