import pytest
from pydantic import ValidationError
from src.shared.configuration_models import IaConfiguration


def test_temperature_casted_from_string():
    cfg = IaConfiguration(temperature="0.75")
    assert cfg.temperature == 0.75


def test_ia_configuration_missing_required_value():
    with pytest.raises(ValidationError):
        IaConfiguration(temperature="not-a-float")


def test_ia_configuration_from_env(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "env-openai")
    monkeypatch.setenv("GEMINI_API_KEY", "env-gemini")
    monkeypatch.setenv("MISTRAL_API_KEY", "env-mistral")

    cfg = IaConfiguration()
    assert cfg.openai_api_key == "env-openai"
    assert cfg.gemini_api_key == "env-gemini"
    assert cfg.mistral_api_key == "env-mistral"
