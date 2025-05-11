import pytest
from unittest.mock import MagicMock, patch

from src.bots.gemini import Gemini
from src.bots.configuration import BotModelConfiguration, BotPersonaConfiguration


@pytest.fixture
def model_config():
    return BotModelConfiguration(
        api_key="fake-api-key",
        model="fake-model",
        temperature=0.6,
        initial_context="Hello Gemini!"
    )


@pytest.fixture
def persona_config(tmp_path):
    prompt_path = tmp_path / "persona.txt"
    prompt_path.write_text("System prompt Gemini")
    return BotPersonaConfiguration(
        persona="Bob",
        prompt_file_path=str(prompt_path)
    )


@patch("src.bots.gemini.genai.GenerativeModel")
def test_set_persona(mock_model, model_config, persona_config):
    mock_chat_session = MagicMock()
    mock_model.return_value.start_chat.return_value = mock_chat_session

    gemini = Gemini(model_config)
    gemini.set_persona(persona_config)

    assert gemini._Gemini__persona == "Bob"
    assert gemini._Gemini__history[0]["parts"] == ["System prompt Gemini"]
    assert gemini._Gemini__history[1]["parts"] == [model_config.initial_context]
    assert gemini._Gemini__service is mock_chat_session


@pytest.mark.asyncio
@patch("src.bots.gemini.genai.GenerativeModel")
async def test_answer_to(mock_model, model_config, persona_config):
    mock_response = MagicMock()
    mock_response.text = "Ceci est une réponse simulée."

    mock_chat_session = MagicMock()
    mock_chat_session.send_message.return_value = mock_response

    mock_model.return_value.start_chat.return_value = mock_chat_session

    gemini = Gemini(model_config)
    gemini.set_persona(persona_config)

    response = await gemini.answer_to("Bonjour !")

    assert response.startswith("\nGEMINI Bob")
    assert "Ceci est une réponse simulée." in response
    mock_chat_session.send_message.assert_called_once_with(
        "Bonjour !",
        generation_config={"temperature": 0.6}
    )
