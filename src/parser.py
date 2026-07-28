import os
import re
from typing import Dict, Optional

class EnvParser:
    @staticmethod
    def parse_file(filepath: str) -> Dict[str, Optional[str]]:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        env_vars: Dict[str, Optional[str]] = {}
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)=(.*)$", line)
                if match:
                    key, val = match.groups()
                    val = val.strip().strip("'\"")
                    env_vars[key] = val if val != "" else None
        return env_vars
