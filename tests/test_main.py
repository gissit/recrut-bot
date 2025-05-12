from unittest.mock import patch, MagicMock
from src import Main
from src.shared import FileContext
from src.bots import (
    Gemini,
    MistralCompletion,
    OpenAIAssistantAPI,
    OpenAICompletionAPI
)


@patch("src.main.FileContext")
@patch("src.main.Gemini")
@patch("src.main.MistralCompletion")
@patch("src.main.OpenAICompletionAPI")
@patch("src.main.OpenAIAssistantAPI")
def test_main_initialization(
    mock_openai_assistant: OpenAIAssistantAPI,
    mock_openai_completion: OpenAICompletionAPI,
    mock_mistral: MistralCompletion,
    mock_gemini: Gemini,
    mock_file_context: FileContext
):
    mock_bot = MagicMock()
    mock_bot.set_persona.return_value = mock_bot

    mock_openai_assistant.return_value = mock_bot
    mock_openai_completion.return_value = mock_bot
    mock_mistral.return_value = mock_bot
    mock_gemini.return_value = mock_bot

    mock_file_context.return_value.get_context.side_effect = [
        "Simulated recruiter context",
        "Simulated candidate context"
    ]

    main_instance = Main()

    assert mock_file_context.call_count == 2
    assert isinstance(main_instance, Main)
