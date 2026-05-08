import json
from pathlib import Path

def  get_mapping():
    base_path = Path(__file__).resolve().parent.parent.parent
    json_path = base_path / "app" / "config" / "mapping.json"
    with open(json_path, "r") as f:
        return json.load(f)
    
