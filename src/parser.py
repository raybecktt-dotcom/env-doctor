import os
import re
from typing import Dict, Optional, Tuple, Any

class EnvParser:
    """Parses .env files into key-value mappings and extracts type annotations."""

    @staticmethod
    def parse_file(filepath: str) -> Dict[str, Dict[str, Any]]:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        env_vars: Dict[str, Dict[str, Any]] = {}
        
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                
                # Check for inline type annotation (# type: int)
                type_match = re.search(r"#\s*type:\s*(\w+)", line, re.IGNORECASE)
                declared_type = type_match.group(1).lower() if type_match else None

                # Clean comments out of the line before splitting key/val
                clean_line = line.split("#")[0].strip()
                match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)=(.*)$", clean_line)
                
                if match:
                    key, val = match.groups()
                    val = val.strip().strip("'\"")
                    env_vars[key] = {
                        "value": val if val != "" else None,
                        "type": declared_type
                    }

        return env_vars
