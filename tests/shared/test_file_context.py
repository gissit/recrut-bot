from unittest.mock import patch, mock_open, MagicMock
from src.shared.file_context import FileContext


@patch("src.shared.file_context.RecursiveCharacterTextSplitter")
@patch("builtins.open", new_callable=mock_open, read_data="This is a sample text file for testing purposes.")
def test_get_context_txt_file(mock_file, mock_splitter):
    mock_splitter.return_value.split_text.return_value = ["Chunk1", "Chunk2", "Chunk3"]

    context = FileContext("document.txt")
    result = context.get_context()

    assert result == "Chunk1\nChunk2\nChunk3"
    mock_file.assert_called_once_with("document.txt", "r", encoding="utf-8")
    mock_splitter.assert_called_once_with(chunk_size=1000, chunk_overlap=200)


@patch("src.shared.file_context.RecursiveCharacterTextSplitter")
@patch("src.shared.file_context.fitz.open")
def test_get_context_pdf_file(mock_fitz_open, mock_splitter):
    mock_doc = MagicMock()
    mock_doc.__iter__.return_value = [
        MagicMock(get_text=MagicMock(return_value="Page1")),
        MagicMock(get_text=MagicMock(return_value="Page2"))
    ]
    mock_fitz_open.return_value = mock_doc
    mock_splitter.return_value.split_text.return_value = ["ChunkPDF1", "ChunkPDF2"]

    context = FileContext("document.pdf")
    result = context.get_context()

    assert result == "ChunkPDF1\nChunkPDF2"
    mock_fitz_open.assert_called_once_with("document.pdf")
    mock_splitter.assert_called_once_with(chunk_size=1000, chunk_overlap=200)
