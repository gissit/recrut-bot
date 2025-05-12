import pytest
from unittest.mock import patch, mock_open, MagicMock
from src.bots import (
    OpenAIAssistantAPI,
    BotModelConfiguration,
    BotPersonaConfiguration
)


@patch("src.bots.openai_assistant_api.OpenAI")
def test_openai_assistant_init(mock_openai):
    cfg = BotModelConfiguration(
        model="gpt-4",
        api_key="fake-key",
        temperature=0.9,
        initial_context="Bonjour"
    )

    instance = OpenAIAssistantAPI(cfg)

    mock_openai.assert_called_once_with(api_key="fake-key")
    assert instance._OpenAIAssistantAPI__initial_context == "Bonjour"


@patch("src.bots.openai_assistant_api.OpenAI")
@patch("builtins.open", new_callable=mock_open, read_data="System instructions")
def test_set_persona(mock_file, mock_openai):
    mock_assistant = MagicMock(id="asst-123")
    mock_thread = MagicMock(id="thread-456")

    client_mock = MagicMock()
    client_mock.beta.assistants.create.return_value = mock_assistant
    client_mock.beta.threads.create.return_value = mock_thread
    mock_openai.return_value = client_mock

    cfg = BotModelConfiguration(
        model="gpt-4",
        api_key="fake",
        temperature=0.5,
        initial_context="Bonjour"
    )
    persona_cfg = BotPersonaConfiguration(
        persona="Alex",
        prompt_file_path="persona.txt"
    )

    api = OpenAIAssistantAPI(cfg)
    result = api.set_persona(persona_cfg)

    assert result is api
    assert api._OpenAIAssistantAPI__assistant_id == "asst-123"
    assert api._OpenAIAssistantAPI__thread_id == "thread-456"


@patch("src.bots.openai_assistant_api.OpenAI")
@pytest.mark.asyncio
async def test_answer_to(mock_openai):
    mock_run = MagicMock(id="run-789", status="completed")
    mock_msg = MagicMock(role="assistant", content=[MagicMock(text=MagicMock(value="  Salut !  "))])
    mock_message_list = MagicMock(data=[mock_msg])

    client = MagicMock()
    client.beta.threads.runs.create.return_value = mock_run
    client.beta.threads.runs.retrieve.return_value = mock_run
    client.beta.threads.messages.list.return_value = mock_message_list

    mock_openai.return_value = client

    cfg = BotModelConfiguration(
        model="gpt-4",
        api_key="key",
        temperature=0.8,
        initial_context="Bonjour"
    )

    api = OpenAIAssistantAPI(cfg)
    api._OpenAIAssistantAPI__assistant_id = "asst-xyz"
    api._OpenAIAssistantAPI__thread_id = "thread-abc"
    api._OpenAIAssistantAPI__persona = "SageBot"

    result = await api.answer_to("Hello")

    assert result == "\nOPENAI ASSISTANT SageBotSalut !"
    client.beta.threads.messages.create.assert_called_once()
    client.beta.threads.runs.create.assert_called_once()
