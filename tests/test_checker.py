import pytest
from src.checker import EnvDoctor

def test_env_doctor_detects_missing_and_empty(tmp_path):
    example = tmp_path / ".env.example"
    example.write_text("DATABASE_URL=\nAPI_KEY=\nPORT=8000\n")

    target = tmp_path / ".env"
    target.write_text("DATABASE_URL=postgres://localhost/db\nAPI_KEY=\n")

    doctor = EnvDoctor(target_path=str(target), example_path=str(example))
    report = doctor.diagnose()

    assert report["healthy"] is False
    assert "PORT" in report["missing"]
    assert "API_KEY" in report["empty"]
