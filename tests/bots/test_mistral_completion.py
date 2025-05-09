import pytest
from unittest.mock import patch, mock_open, MagicMock
from src.bots.mistral_completion import MistralCompletion
from src.bots.configuration import BotModelConfiguration, BotPersonaConfiguration


@patch("src.bots.mistral_completion.Mistral")
def test_mistral_initialization(mock_mistral):
    cfg = BotModelConfiguration(
        model="mistral-tiny",
        api_key="fake-key",
        temperature=0.6,
        initial_context="Bonjour"
    )

    mistral = MistralCompletion(cfg)

    mock_mistral.assert_called_once_with(api_key="fake-key")
    assert mistral._MistralCompletion__history[0].content == "Bonjour"


@patch("builtins.open", new_callable=mock_open, read_data="System prompt for Mistral")
@patch("src.bots.mistral_completion.Mistral")
def test_mistral_set_persona(mock_mistral, mock_file):
    cfg = BotModelConfiguration(
        model="mistral-tiny",
        api_key="fake-key",
        temperature=0.6,
        initial_context="Context"
    )
    persona_cfg = BotPersonaConfiguration(
        persona="M1",
        prompt_file_path="persona.txt"
    )

    mistral = MistralCompletion(cfg)
    result = mistral.set_persona(persona_cfg)

    assert result is mistral
    assert mistral._MistralCompletion__persona == "M1"
    assert mistral._MistralCompletion__history[0].role == "system"
    assert mistral._MistralCompletion__history[0].content == "System prompt for Mistral"


@patch("src.bots.mistral_completion.Mistral")
@patch("builtins.open", new_callable=mock_open, read_data="System prompt")
@pytest.mark.asyncio
async def test_mistral_answer_to(mock_file, mock_mistral):
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content=" The response "))
    ]
    mock_mistral.return_value.chat.complete.return_value = mock_response

    model_cfg = BotModelConfiguration(
        model="mistral-tiny",
        api_key="key",
        temperature=0.5,
        initial_context="Bonjour"
    )
    persona_cfg = BotPersonaConfiguration(
        persona="X",
        prompt_file_path="prompt.txt"
    )

    mistral = MistralCompletion(model_cfg).set_persona(persona_cfg)
    result = await mistral.answer_to("What is your name?")

    assert result == "\nMISTRAL XThe response"
    mock_mistral.return_value.chat.complete.assert_called_once()
