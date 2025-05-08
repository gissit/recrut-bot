import pytest
from unittest.mock import patch, mock_open, MagicMock
from src.bots.gemini import Gemini
from src.bots.configuration import BotModelConfiguration, BotPersonaConfiguration


@patch("src.bots.gemini.genai.configure")
def test_gemini_init(mock_configure):
    cfg = BotModelConfiguration(
        model="gemini-pro",
        api_key="fake-api-key",
        temperature=0.7,
        initial_context="Hello Gemini"
    )

    gem = Gemini(cfg)

    mock_configure.assert_called_once_with(api_key="fake-api-key")

    assert gem._Gemini__history == [{"role": "user", "parts": ["Hello Gemini"]}]


@patch("src.bots.gemini.genai.GenerativeModel")
@patch("builtins.open", new_callable=mock_open, read_data="System prompt text")
def test_gemini_set_persona(mock_file, mock_generative_model):
    mock_chat_session = MagicMock()
    mock_generative_model.return_value.start_chat.return_value = mock_chat_session

    persona_cfg = BotPersonaConfiguration(
        persona="DrBot",
        prompt_file_path="persona.txt"
    )

    model_cfg = BotModelConfiguration(
        model="gemini-pro",
        api_key="fake-api-key",
        temperature=0.7,
        initial_context="Hello Gemini"
    )

    gem = Gemini(model_cfg)
    result = gem.set_persona(persona_cfg)

    assert result is gem
    assert gem._Gemini__persona == "DrBot"
    assert mock_file.called
    mock_generative_model.assert_called_once_with(model_name="gemini-pro")
    mock_generative_model.return_value.start_chat.assert_called_once()


@patch("src.bots.gemini.genai.GenerativeModel")
@patch("builtins.open", new_callable=mock_open, read_data="System prompt")
@pytest.mark.asyncio
async def test_gemini_answer_to(mock_file, mock_generative_model):
    mock_chat_session = MagicMock()
    mock_chat_session.send_message.return_value.text = "  The answer.  "
    mock_generative_model.return_value.start_chat.return_value = mock_chat_session

    model_cfg = BotModelConfiguration(
        model="gemini-pro",
        api_key="fake",
        temperature=0.5,
        initial_context="Hi"
    )
    persona_cfg = BotPersonaConfiguration(
        persona="X",
        prompt_file_path="prompt.txt"
    )

    gem = Gemini(model_cfg).set_persona(persona_cfg)
    response = await gem.answer_to("Tell me something")

    assert response == "\nGEMINI XThe answer."
    mock_chat_session.send_message.assert_called_once_with(
        "Tell me something",
        generation_config={"temperature": 0.5}
    )
