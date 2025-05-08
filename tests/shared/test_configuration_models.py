import pytest
import os

from unittest.mock import patch
from pydantic import ValidationError
from src.shared.configuration_models import IaConfiguration


def test_temperature_casted_from_string():
    cfg = IaConfiguration(temperature="0.75")
    assert cfg.temperature == 0.75


def test_ia_configuration_missing_required_value():
    with pytest.raises(ValidationError):
        IaConfiguration(temperature="not-a-float")


@patch.dict(os.environ, {
    "OPENAI_API_KEY": "env-openai",
    "GEMINI_API_KEY": "env-gemini",
    "MISTRAL_API_KEY": "env-mistral"
})
def test_ia_configuration_from_env():
    cfg = IaConfiguration()
    assert cfg.openai_api_key == "env-openai"
    assert cfg.gemini_api_key == "env-gemini"
    assert cfg.mistral_api_key == "env-mistral"
