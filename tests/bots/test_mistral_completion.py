import pytest
from unittest.mock import MagicMock

from src.bots.mistral_completion import MistralCompletion
from src.bots.configuration import BotModelConfiguration, BotPersonaConfiguration
from mistralai import SystemMessage, UserMessage


@pytest.fixture
def model_config():
    return BotModelConfiguration(
        api_key="fake-api-key",
        model="fake-model",
        temperature=0.7,
        initial_context="Hello from user"
    )


@pytest.fixture
def persona_config(tmp_path):
    prompt_path = tmp_path / "persona.txt"
    prompt_path.write_text("System prompt content")
    return BotPersonaConfiguration(
        persona="TestBot",
        prompt_file_path=str(prompt_path)
    )


def test_set_persona(model_config, persona_config):
    bot = MistralCompletion(model_config)

    bot.set_persona(persona_config)

    history = bot._MistralCompletion__history
    assert isinstance(history[0], SystemMessage)
    assert isinstance(history[1], UserMessage)
    assert history[0].content == "System prompt content"
    assert history[1].content == model_config.initial_context


@pytest.mark.asyncio
async def test_answer_to(model_config, persona_config):
    bot = MistralCompletion(model_config)
    bot.set_persona(persona_config)

    fake_response = MagicMock()
    fake_response.choices = [
        MagicMock(message=UserMessage(content="Mocked response from Mistral"))
    ]

    mocked_service = MagicMock()
    mocked_service.chat.complete.return_value = fake_response

    bot._MistralCompletion__service = mocked_service

    result = await bot.answer_to("Hello bot!")

    assert "Mocked response from Mistral" in result
    assert result.startswith("\nMISTRAL TestBot")
    assert isinstance(bot._MistralCompletion__history[-1], UserMessage)
