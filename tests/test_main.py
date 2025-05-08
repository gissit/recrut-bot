from unittest.mock import patch
from src import Main
from src.shared.file_context import FileContext


@patch("src.main.FileContext")
def test_main_initialization(mock_file_context: FileContext):
    mock_file_context.return_value.get_context.side_effect = [
        "Simulated recruiter context",
        "Simulated candidate context"
    ]

    main_instance = Main()

    assert mock_file_context.call_count == 2
    assert isinstance(main_instance, Main)
