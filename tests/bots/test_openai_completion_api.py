import pytest
from unittest.mock import MagicMock, patch

from src.bots import (
    OpenAICompletionAPI,
    BotModelConfiguration,
    BotPersonaConfiguration
)


@pytest.fixture
def model_config():
    return BotModelConfiguration(
        api_key="fake-api-key",
        model="gpt-fake-model",
        temperature=0.5,
        initial_context="Bonjour, je suis un utilisateur."
    )


@pytest.fixture
def persona_config(tmp_path):
    prompt_file = tmp_path / "prompt.txt"
    prompt_file.write_text("Vous etes un assistant utile.")
    return BotPersonaConfiguration(
        persona="Alice",
        prompt_file_path=str(prompt_file)
    )


def test_set_persona(model_config, persona_config):
    instance = OpenAICompletionAPI(model_config)
    instance.set_persona(persona_config)

    history = instance._OpenAICompletionAPI__history
    assert history[0]["role"] == "system"
    assert history[0]["content"] == "Vous etes un assistant utile."
    assert history[1]["role"] == "user"
    assert history[1]["content"] == model_config.initial_context
    assert instance._OpenAICompletionAPI__persona == "Alice"


@pytest.mark.asyncio
@patch("src.bots.openai_completion_api.OpenAI")
async def test_answer_to(mock_openai, model_config, persona_config):
    # Préparer la réponse simulée
    fake_message = MagicMock()
    fake_message.content = "Réponse de test."
    fake_message.role = "assistant"

    fake_choice = MagicMock()
    fake_choice.message = fake_message

    fake_response = MagicMock()
    fake_response.choices = [fake_choice]

    mock_instance = mock_openai.return_value
    mock_instance.chat.completions.create.return_value = fake_response

    instance = OpenAICompletionAPI(model_config)
    instance.set_persona(persona_config)

    result = await instance.answer_to("Quel temps fait-il ?")

    assert result.startswith("\nOPENAI COMPLETION Alice")
    assert "Réponse de test." in result

    last_message = instance._OpenAICompletionAPI__history[-1]
    assert last_message.role == "assistant"
    assert last_message.content == "Réponse de test."

    mock_instance.chat.completions.create.assert_called_once()
    args, kwargs = mock_instance.chat.completions.create.call_args

    assert kwargs["model"] == model_config.model
    assert kwargs["temperature"] == model_config.temperature

    messages = kwargs["messages"]
    assert isinstance(messages, list)
    assert messages[-2]["content"] == "Quel temps fait-il ?"
