import pytest
from unittest.mock import patch, mock_open, MagicMock
from src.bots.openai_completion_api import OpenAICompletionAPI
from src.bots.configuration import BotModelConfiguration, BotPersonaConfiguration


@patch("src.bots.openai_completion_api.OpenAI")
def test_openai_completion_init(mock_openai):
    cfg = BotModelConfiguration(
        model="gpt-3.5",
        api_key="test-key",
        temperature=0.7,
        initial_context="Bonjour"
    )

    api = OpenAICompletionAPI(cfg)

    mock_openai.assert_called_once_with(api_key="test-key")


@patch("src.bots.openai_completion_api.OpenAI")
@patch("builtins.open", new_callable=mock_open, read_data="System instruction")
def test_set_persona(mock_file, mock_openai):
    cfg = BotModelConfiguration(
        model="gpt-3.5",
        api_key="test-key",
        temperature=0.7,
        initial_context="Init context"
    )
    persona_cfg = BotPersonaConfiguration(
        persona="Alex",
        prompt_file_path="persona.txt"
    )

    api = OpenAICompletionAPI(cfg)
    result = api.set_persona(persona_cfg)

    assert result is api
    assert api._OpenAICompletionAPI__persona == "Alex"
    assert api._OpenAICompletionAPI__history[0]["role"] == "system"
    assert api._OpenAICompletionAPI__history[0]["content"] == "System instruction"


@patch("src.bots.openai_completion_api.OpenAI")
@pytest.mark.asyncio
async def test_answer_to(mock_openai):
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content="  Hello world!  "))
    ]
    mock_openai.return_value.chat.completions.create.return_value = mock_response

    cfg = BotModelConfiguration(
        model="gpt-3.5",
        api_key="fake",
        temperature=0.6,
        initial_context="Bonjour"
    )

    api = OpenAICompletionAPI(cfg)
    api._OpenAICompletionAPI__persona = "AI"
    result = await api.answer_to("Salut")

    assert result == "\nOPENAI COMPLETION AIHello world!"
    mock_openai.return_value.chat.completions.create.assert_called_once()
