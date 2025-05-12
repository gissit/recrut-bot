from unittest.mock import patch, mock_open, MagicMock
from src.shared import FileContext


def test_extract_text_from_txt():
    mock_data = "This is a test txt file."
    with patch("builtins.open", mock_open(read_data=mock_data)) as mocked_file:
        fc = FileContext("test.txt")
        result = fc.get_context()
        assert mock_data in result
        mocked_file.assert_called_once_with("test.txt", "r", encoding="utf-8")


def test_extract_text_from_pdf():
    mock_page1 = MagicMock(get_text=lambda: "Page 1 text")
    mock_page2 = MagicMock(get_text=lambda: "Page 2 text")
    mock_doc = [mock_page1, mock_page2]

    with patch("fitz.open", return_value=mock_doc) as mocked_fitz:
        fc = FileContext("test.pdf")
        result = fc.get_context()
        assert "Page 1 text" in result
        assert "Page 2 text" in result
        mocked_fitz.assert_called_once_with("test.pdf")
