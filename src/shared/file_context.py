import fitz
from langchain.text_splitter import RecursiveCharacterTextSplitter


class FileContext():
    __path: str = ""

    def __init__(self, path: str = ""):
        self.__path = path

    def _extract_text_from_pdf(self):
        doc = fitz.open(self.__path)
        return "\n".join(page.get_text() for page in doc)

    def _extract_text_from_txt(self):
        with open(self.__path, "r", encoding="utf-8") as f:
            return f.read()

    def _split_text(self, text, chunk_size=1000, overlap=200):
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
        return splitter.split_text(text)

    def _get_chunks(self):
        if self.__path.endswith(".pdf"):
            raw = self._extract_text_from_pdf()
        else:
            raw = self._extract_text_from_txt()

        return self._split_text(raw)

    def get_context(self) -> str:
        return "\n".join([f"{chunk}" for chunk in self._get_chunks()])
