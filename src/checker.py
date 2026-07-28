import re
from typing import Dict, Any, List
from src.parser import EnvParser

SENSITIVE_PATTERNS = [r"SECRET", r"PASSWORD", r"PRIVATE_KEY", r"API_KEY", r"TOKEN", r"AUTH"]
WEAK_VALUES = {"admin", "password", "123456", "secret", "root", "test", "change_me"}

class EnvDoctor:
    def __init__(self, target_path: str, example_path: str):
        self.target_path = target_path
        self.example_path = example_path

    def _validate_type(self, value: str, expected_type: str) -> bool:
        if not expected_type or not value:
            return True
        if expected_type in ("int", "integer"):
            return value.isdigit() or (value.startswith("-") and value[1:].isdigit())
        if expected_type in ("bool", "boolean"):
            return value.lower() in ("true", "false", "1", "0")
        if expected_type == "url":
            return value.startswith(("http://", "https://", "postgres://", "mongodb://"))
        return True

    def _scan_secrets(self, target_vars: Dict[str, Dict[str, Any]]) -> List[str]:
        flagged = []
        for key, data in target_vars.items():
            val = data["value"]
            if not val:
                continue
            if any(re.search(pat, key, re.IGNORECASE) for pat in SENSITIVE_PATTERNS):
                if val.lower() in WEAK_VALUES or len(val) < 8:
                    flagged.append(key)
        return flagged

    def diagnose(self) -> Dict[str, Any]:
        target_vars = EnvParser.parse_file(self.target_path)
        example_vars = EnvParser.parse_file(self.example_path)

        missing_keys = [k for k in example_vars if k not in target_vars]
        empty_keys = [k for k in example_vars if k in target_vars and target_vars[k]["value"] is None]
        extra_keys = [k for k in target_vars if k not in example_vars]

        # Type validation
        invalid_types = []
        for k, exp_data in example_vars.items():
            expected_type = exp_data["type"]
            if k in target_vars and target_vars[k]["value"] is not None and expected_type:
                if not self._validate_type(target_vars[k]["value"], expected_type):
                    invalid_types.append({"key": k, "expected": expected_type, "got": target_vars[k]["value"]})

        # Secret scanning
        weak_secrets = self._scan_secrets(target_vars)

        healthy = (len(missing_keys) == 0 and len(empty_keys) == 0 and 
                   len(invalid_types) == 0 and len(weak_secrets) == 0)

        return {
            "healthy": healthy,
            "missing": missing_keys,
            "empty": empty_keys,
            "extra": extra_keys,
            "invalid_types": invalid_types,
            "weak_secrets": weak_secrets
        }
