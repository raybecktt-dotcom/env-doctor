from typing import Dict, Any
from src.parser import EnvParser

class EnvDoctor:
    def __init__(self, target_path: str, example_path: str):
        self.target_path = target_path
        self.example_path = example_path

    def diagnose(self) -> Dict[str, Any]:
        target_vars = EnvParser.parse_file(self.target_path)
        example_vars = EnvParser.parse_file(self.example_path)

        # Missing: Key is defined in example, but absent in target
        missing_keys = [k for k in example_vars if k not in target_vars]

        # Empty: Key is in example and present in target, but target value is None/blank
        empty_keys = [k for k in example_vars if k in target_vars and target_vars[k] is None]

        # Extra: Key exists in target, but not listed in example
        extra_keys = [k for k in target_vars if k not in example_vars]

        return {
            "healthy": len(missing_keys) == 0 and len(empty_keys) == 0,
            "missing": missing_keys,
            "empty": empty_keys,
            "extra": extra_keys,
        }
