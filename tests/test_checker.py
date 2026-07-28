import pytest
from src.checker import EnvDoctor

def test_env_doctor_full_audit(tmp_path):
    example = tmp_path / ".env.example"
    example.write_text("PORT=8000 # type: int\nAPI_KEY=\nSECRET_KEY=\n")

    target = tmp_path / ".env"
    target.write_text("PORT=not_a_number\nAPI_KEY=\nSECRET_KEY=12345\n")

    doctor = EnvDoctor(target_path=str(target), example_path=str(example))
    report = doctor.diagnose()

    assert report["healthy"] is False
    assert "API_KEY" in report["empty"]
    assert any(item["key"] == "PORT" for item in report["invalid_types"])
    assert "SECRET_KEY" in report["weak_secrets"]
